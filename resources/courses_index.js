/* global DATA */
const ICON_PDF = '<svg viewBox="0 0 24 24" fill="none" stroke="#d32f2f" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><text x="12" y="17" text-anchor="middle" font-size="6" fill="#d32f2f" stroke="none" font-weight="bold">PDF</text></svg>';

let currentFolder = "";

const breadcrumbEl = document.getElementById("breadcrumb");
const subfoldersEl = document.getElementById("subfolders");
const searchEl = document.getElementById("search");
const slidesEl = document.getElementById("filter-slides");
const sort1El = document.getElementById("sort-primary");
const sort1DirEl = document.getElementById("sort-primary-dir");
const resultsEl = document.getElementById("results");
const totalEl = document.getElementById("total-count");
const numbersEl = document.getElementById("show-numbers");

const ALL_SLIDE_COUNTS = [...new Set(DATA.map(e => e.slides).filter(s => s > 0))].sort((a, b) => a - b);
slidesEl.innerHTML = '<option value="">All sizes</option>' +
    ALL_SLIDE_COUNTS.map(s => '<option value="' + s + '">' + s + ' slides</option>').join("");

document.querySelector('label[for="filter-slides"]').textContent =
    "Slides (" + ALL_SLIDE_COUNTS.length + "):";

function navigateFolder(folder) {
    currentFolder = folder;
    history.pushState(null, "", folder ? "#folder=" + encodeURIComponent(folder) : "#");
    render();
    window.scrollTo(0, 0);
}

function getSubfolders(folder, entries) {
    const prefix = folder ? folder + "/" : "";
    const subs = new Map();
    for (const e of entries) {
        const path = e.folder;
        if (folder && !path.startsWith(prefix)) continue;
        if (!folder && !path) continue;
        const rest = folder ? path.substring(prefix.length) : path;
        if (!rest) continue;
        const slash = rest.indexOf("/");
        if (slash === -1) continue;
        const sub = rest.substring(0, slash);
        subs.set(sub, (subs.get(sub) || 0) + 1);
    }
    return [...subs.entries()].sort((a, b) => a[0].localeCompare(b[0]));
}

function renderBreadcrumb() {
    if (!currentFolder) {
        breadcrumbEl.innerHTML = '<span class="breadcrumb-current">All Courses</span>';
        return;
    }
    const parts = currentFolder.split("/");
    let html = '<a href="#" onclick="navigateFolder(\'\'); return false;">All Courses</a>';
    for (let i = 0; i < parts.length; i++) {
        const path = parts.slice(0, i + 1).join("/");
        const label = parts[i].replace(/_/g, " ").replace(/-/g, " ");
        html += '<span class="breadcrumb-sep">&gt;</span>';
        if (i === parts.length - 1) {
            html += '<span class="breadcrumb-current">' + label + '</span>';
        } else {
            html += '<a href="#" onclick="navigateFolder(\'' + path.replace(/'/g, "\\'") + '\'); return false;">' + label + '</a>';
        }
    }
    breadcrumbEl.innerHTML = html;
}

function renderSubfolders(filtered) {
    const subs = getSubfolders(currentFolder, filtered);
    if (subs.length === 0) {
        subfoldersEl.innerHTML = "";
        return;
    }
    subfoldersEl.innerHTML = subs.map(function(s) {
        var name = s[0];
        var count = s[1];
        var path = currentFolder ? currentFolder + "/" + name : name;
        var label = name.replace(/_/g, " ").replace(/-/g, " ");
        return '<a class="subfolder-card" href="#" onclick="navigateFolder(\'' +
            path.replace(/'/g, "\\'") + '\'); return false;">' +
            label + ' <span class="subfolder-count">(' + count + ')</span></a>';
    }).join("");
}

function render() {
    const search = searchEl.value.toLowerCase();
    const slidesFilter = slidesEl.value;
    const sort1 = sort1El.value;
    const sort1Dir = sort1DirEl.value === "asc" ? 1 : -1;

    renderBreadcrumb();

    const isSearching = search.length > 0 || slidesFilter;
    const filtered = DATA.filter(e => {
        if (!isSearching && currentFolder) {
            if (!e.folder.startsWith(currentFolder + "/") && e.folder !== currentFolder) return false;
        }
        if (!isSearching && !currentFolder) {
            return false;
        }
        if (search && !e.name.toLowerCase().includes(search)) return false;
        if (slidesFilter && e.slides !== parseInt(slidesFilter)) return false;
        return true;
    });
    const directChildren = isSearching ? filtered : filtered.filter(e => {
        const prefix = currentFolder ? currentFolder + "/" : "";
        const rest = e.folder.substring(prefix.length);
        return rest.indexOf("/") === -1;
    });
    const allInFolder = DATA.filter(e => {
        if (currentFolder) {
            return e.folder.startsWith(currentFolder + "/") || e.folder === currentFolder;
        }
        return true;
    });

    const statsSource = isSearching ? filtered : allInFolder;
    const totalChapters = statsSource.reduce((s, e) => s + (e.chapters || 0), 0);
    const totalSlides = statsSource.reduce((s, e) => s + (e.slides || 0), 0);
    totalEl.innerHTML = statsSource.length + " courses, " +
        '<span class="stat-chapters">' + totalChapters + " chapters</span>, " +
        '<span class="stat-slides">' + totalSlides + " slides</span>";
    renderSubfolders(allInFolder);

    const getVal = (e, key) => {
        if (key === "name") return e.name;
        if (key === "slides") return e.slides || 0;
        if (key === "folder") return e.folder;
        return e[key];
    };

    const getLabel = (e, key) => {
        if (key === "folder") return e.folder_label || "Root";
        if (key === "slides") return e.slides + " slides";
        if (key === "chapters") return e.chapters + " chapters";
        if (key === "name") return "All Courses";
        return "";
    };

    directChildren.sort((a, b) => {
        const v1a = getVal(a, sort1);
        const v1b = getVal(b, sort1);
        if (v1a !== v1b) {
            const res = (typeof v1a === "string") ? v1a.localeCompare(v1b) : v1a - v1b;
            return res * sort1Dir;
        }
        return a.name.localeCompare(b.name);
    });

    const groups = [];
    let lastHeader = null;
    for (const item of directChildren) {
        const h = getLabel(item, sort1);
        if (h !== lastHeader) {
            groups.push({ label: h, items: [] });
            lastHeader = h;
        }
        groups[groups.length - 1].items.push(item);
    }

    let html = "";
    if (groups.length === 0) {
        html = '<p class="no-results">No courses match the current filters.</p>';
    }
    for (const group of groups) {
        html += "<h2>" + group.label + ' <span class="count">(' + group.items.length + ")</span></h2><ul>";
        const showNumbers = numbersEl.checked;
        for (let i = 0; i < group.items.length; i++) {
            const item = group.items[i];
            const numPrefix = showNumbers ? '<span class="course-number">' + (i + 1) + ".</span> " : "";
            const chaptersBadge = item.chapters ? '<span class="chapters-badge">' + item.chapters + " chapters</span>" : "";
            const slidesBadge = item.slides ? '<span class="slides-badge">' + item.slides + " slides</span>" : "";
            const pdfLink = item.pdf ? '<a class="dl-icon" href="' + item.pdf + '" download title="Download PDF">' + ICON_PDF + "</a>" : "";
            const nameHtml = item.pdf ? '<a href="' + item.pdf + '" target="_blank">' + item.name + "</a>" : "<span>" + item.name + "</span>";
            html += "<li>" + numPrefix + nameHtml + chaptersBadge + slidesBadge + " " + pdfLink + "</li>";
        }
        html += "</ul>";
    }
    resultsEl.innerHTML = html;
}

// Autocomplete
const acList = document.getElementById("autocomplete-list");
let acIndex = -1;

function updateAutocomplete() {
    const query = searchEl.value.toLowerCase();
    acIndex = -1;
    if (query.length < 2) {
        acList.classList.remove("visible");
        return;
    }
    const matches = DATA.filter(e => e.name.toLowerCase().includes(query)).slice(0, 10);
    if (matches.length === 0) {
        acList.classList.remove("visible");
        return;
    }
    acList.innerHTML = matches.map((m, i) =>
        '<div class="autocomplete-item" data-index="' + i + '">' +
        m.name + '<span class="ac-folder">' + m.folder_label + '</span></div>'
    ).join("");
    acList.classList.add("visible");
}

acList.addEventListener("mousedown", function(ev) {
    var item = ev.target.closest(".autocomplete-item");
    if (item) {
        acList.classList.remove("visible");
        var idx = parseInt(item.dataset.index);
        var query = searchEl.value.toLowerCase();
        var matches = DATA.filter(e => e.name.toLowerCase().includes(query));
        if (matches[idx]) {
            searchEl.value = matches[idx].name;
            render();
        }
    }
});

searchEl.addEventListener("keydown", function(ev) {
    var items = acList.querySelectorAll(".autocomplete-item");
    if (!acList.classList.contains("visible") || items.length === 0) return;
    if (ev.key === "ArrowDown") {
        ev.preventDefault();
        acIndex = Math.min(acIndex + 1, items.length - 1);
    } else if (ev.key === "ArrowUp") {
        ev.preventDefault();
        acIndex = Math.max(acIndex - 1, 0);
    } else if (ev.key === "Enter" && acIndex >= 0) {
        ev.preventDefault();
        acList.classList.remove("visible");
        var query = searchEl.value.toLowerCase();
        var matches = DATA.filter(e => e.name.toLowerCase().includes(query));
        if (matches[acIndex]) {
            searchEl.value = matches[acIndex].name;
            render();
        }
        return;
    } else if (ev.key === "Escape") {
        acList.classList.remove("visible");
        return;
    } else {
        return;
    }
    items.forEach(function(el, i) {
        el.classList.toggle("active", i === acIndex);
    });
});

searchEl.addEventListener("blur", function() {
    setTimeout(function() { acList.classList.remove("visible"); }, 150);
});

searchEl.addEventListener("input", function() {
    updateAutocomplete();
    render();
});
slidesEl.addEventListener("change", render);
numbersEl.addEventListener("change", render);
sort1El.addEventListener("change", render);
sort1DirEl.addEventListener("change", render);

window.addEventListener("popstate", function() {
    var hash = location.hash;
    if (hash && hash.startsWith("#folder=")) {
        currentFolder = decodeURIComponent(hash.substring(8));
    } else {
        currentFolder = "";
    }
    render();
});

if (location.hash && location.hash.startsWith("#folder=")) {
    currentFolder = decodeURIComponent(location.hash.substring(8));
}
render();
