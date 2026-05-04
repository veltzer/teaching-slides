/* global DATA */
const ICON_PDF = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><text x="12" y="17" text-anchor="middle" font-size="6" fill="currentColor" stroke="none" font-weight="bold">PDF</text></svg>';

let currentFolder = "";

const breadcrumbEl = document.getElementById("breadcrumb");
const subfoldersEl = document.getElementById("subfolders");
const searchEl = document.getElementById("search");
const levelEl = document.getElementById("filter-level");
const categoryEl = document.getElementById("filter-category");
const typeEl = document.getElementById("filter-type");
const tagEl = document.getElementById("filter-tag");
const audienceEl = document.getElementById("filter-audience");
const durationEl = document.getElementById("filter-duration");
const numbersEl = document.getElementById("show-numbers");
const sort1El = document.getElementById("sort-primary");
const sort1DirEl = document.getElementById("sort-primary-dir");
const sort2El = document.getElementById("sort-secondary");
const sort2DirEl = document.getElementById("sort-secondary-dir");
const resultsEl = document.getElementById("results");
const totalEl = document.getElementById("total-count");

// Compute duration days
DATA.forEach(e => {
    e.dh = e.duration_hours || 0;
    e.duration_days = e.dh ? Math.round(e.dh / 8) : 0;
});

// Populate duration filter
const ALL_DURATION_DAYS = [...new Set(DATA.map(e => e.duration_days).filter(d => d > 0))].sort((a, b) => a - b);
durationEl.innerHTML = '<option value="">All durations</option>' +
    ALL_DURATION_DAYS.map(d => '<option value="' + d + '">' + d + (d === 1 ? " day" : " days") + " / " + (d * 8) + "h</option>").join("");

// Update filter labels with counts
document.querySelector('label[for="filter-level"]').textContent =
    "Level (" + new Set(DATA.map(e => e.level).filter(Boolean)).size + "):";
document.querySelector('label[for="filter-category"]').textContent =
    "Category (" + new Set(DATA.map(e => e.category).filter(Boolean)).size + "):";
document.querySelector('label[for="filter-type"]').textContent =
    "Type (" + new Set(DATA.map(e => e.type).filter(Boolean)).size + "):";
document.querySelector('label[for="filter-tag"]').textContent =
    "Tag (" + new Set(DATA.flatMap(e => e.tags)).size + "):";
document.querySelector('label[for="filter-duration"]').textContent =
    "Duration (" + ALL_DURATION_DAYS.length + "):";
document.querySelector('label[for="filter-audience"]').textContent =
    "Audience (" + new Set(DATA.flatMap(e => e.audience)).size + "):";

function navigateFolder(folder) {
    currentFolder = folder;
    history.pushState(null, "", folder ? "#folder=" + encodeURIComponent(folder) : "#");
    render();
    window.scrollTo(0, 0);
}

function renderBreadcrumb() {
    if (!currentFolder) {
        breadcrumbEl.innerHTML = '<span class="breadcrumb-current">All Items</span>';
        return;
    }
    const parts = currentFolder.split("/");
    let html = '<a href="#" onclick="navigateFolder(\'\'); return false;">All Items</a>';
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

function getSubfolders(folder, entries) {
    const prefix = folder ? folder + "/" : "";
    const subs = new Map();
    for (const e of entries) {
        const path = e.folder;
        if (prefix && !path.startsWith(prefix)) continue;
        const rest = prefix ? path.substring(prefix.length) : path;
        if (!rest) continue;
        const slash = rest.indexOf("/");
        if (slash === -1) continue;
        const sub = rest.substring(0, slash);
        subs.set(sub, (subs.get(sub) || 0) + 1);
    }
    return [...subs.entries()].sort((a, b) => a[0].localeCompare(b[0]));
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
    const level = levelEl.value;
    const category = categoryEl.value;
    const type = typeEl.value;
    const tag = tagEl.value;
    const audience = audienceEl.value;
    const duration = durationEl.value;
    const sort1 = sort1El.value;
    const sort1Dir = sort1DirEl.value === "asc" ? 1 : -1;
    const sort2 = sort2El.value;
    const sort2Dir = sort2DirEl.value === "asc" ? 1 : -1;

    renderBreadcrumb();

    const filtered = DATA.filter(e => {
        if (currentFolder) {
            if (!e.folder.startsWith(currentFolder + "/") && e.folder !== currentFolder) return false;
        }
        if (search && !e.name.toLowerCase().includes(search)) return false;
        if (level && e.level !== level) return false;
        if (category && e.category !== category) return false;
        if (type && e.type !== type) return false;
        if (tag && !e.tags.includes(tag)) return false;
        if (audience && !e.audience.includes(audience)) return false;
        if (duration && e.duration_days !== parseInt(duration)) return false;
        return true;
    });

    const totalChapters = filtered.reduce((s, e) => s + (e.chapters || 0), 0);
    const totalSlides = filtered.reduce((s, e) => s + (e.slides || 0), 0);
    const nCourses = filtered.filter(e => e.type === "course").length;
    const nLectures = filtered.filter(e => e.type === "lecture").length;
    totalEl.innerHTML = nCourses + " courses, " + nLectures + " lectures, " +
        '<span class="stat-chapters">' + totalChapters + " chapters</span>, " +
        '<span class="stat-slides">' + totalSlides + " slides</span>";
    renderSubfolders(filtered);

    const LEVEL_ORDER = {beginner: 0, intermediate: 1, advanced: 2};
    const getVal = (e, key) => {
        if (key === "name") return e.name;
        if (key === "slides") return e.slides || 0;
        if (key === "chapters") return e.chapters || 0;
        if (key === "folder") { const p = e.folder.split("/"); return p.length > 1 ? p.slice(0, -1).join("/") : ""; }
        if (key === "level") return LEVEL_ORDER[e.level] ?? 3;
        if (key === "category") return e.category || "";
        if (key === "duration") return e.dh || 0;
        return e[key];
    };

    const getLabel = (e, key) => {
        if (key === "folder") {
            const parts = e.folder.split("/");
            if (parts.length <= 1) return "Root";
            return parts.slice(0, -1).map(p => p.replace(/_/g, " ").replace(/-/g, " ").replace(/\b\w/g, c => c.toUpperCase())).join(" / ");
        }
        if (key === "level") return (e.level || "No Level").charAt(0).toUpperCase() + (e.level || "No Level").slice(1);
        if (key === "category") return (e.category || "No Category").replace(/-/g, " ").replace(/\b\w/g, c => c.toUpperCase());
        if (key === "duration") return e.dh ? e.duration_days + "d / " + e.dh + "h" : "No Duration";
        if (key === "slides") return e.slides + " slides";
        if (key === "chapters") return e.chapters + " chapters";
        if (key === "name") return "All Items";
        return "";
    };

    filtered.sort((a, b) => {
        const v1a = getVal(a, sort1);
        const v1b = getVal(b, sort1);
        if (v1a !== v1b) {
            const res = (typeof v1a === "string") ? v1a.localeCompare(v1b) : v1a - v1b;
            return res * sort1Dir;
        }
        const v2a = getVal(a, sort2);
        const v2b = getVal(b, sort2);
        if (v2a !== v2b) {
            const res = (typeof v2a === "string") ? v2a.localeCompare(v2b) : v2a - v2b;
            return res * sort2Dir;
        }
        return a.name.localeCompare(b.name);
    });

    const groups = [];
    let lastHeader = null;
    for (const item of filtered) {
        const h = getLabel(item, sort1);
        const folderKey = sort1 === "folder" ? getVal(item, "folder") : "";
        if (h !== lastHeader) {
            groups.push({ label: h, folderKey: folderKey, items: [] });
            lastHeader = h;
        }
        groups[groups.length - 1].items.push(item);
    }

    let html = "";
    if (groups.length === 0) {
        html = '<p class="no-results">No items match the current filters.</p>';
    }
    const showNumbers = numbersEl.checked;
    let globalNum = 0;
    for (const group of groups) {
        const groupChapters = group.items.reduce((s, e) => s + (e.chapters || 0), 0);
        const groupSlides = group.items.reduce((s, e) => s + (e.slides || 0), 0);
        let headerLabel = group.label;
        if (group.folderKey) {
            const fParts = group.folderKey.split("/");
            headerLabel = fParts.map((p, idx) => {
                const path = fParts.slice(0, idx + 1).join("/");
                const label = p.replace(/_/g, " ").replace(/-/g, " ").replace(/\b\w/g, c => c.toUpperCase());
                return '<a href="#" onclick="navigateFolder(\'' + path.replace(/'/g, "\\'") + '\'); return false;">' + label + '</a>';
            }).join(' <span class="breadcrumb-sep">/</span> ');
        }
        const gc = group.items.filter(e => e.type === "course").length;
        const gl = group.items.filter(e => e.type === "lecture").length;
        const groupLabel = [gc ? gc + " courses" : "", gl ? gl + " lectures" : ""].filter(Boolean).join(", ");
        html += '<h2>' + headerLabel +
            ' <span class="count">(' + groupLabel + ', ' +
            '<span class="stat-chapters">' + groupChapters + ' chapters</span>, ' +
            '<span class="stat-slides">' + groupSlides + ' slides</span>)</span></h2><ul>';
        for (let i = 0; i < group.items.length; i++) {
            globalNum++;
            const item = group.items[i];
            const numPrefix = showNumbers ? '<span class="course-number">' + globalNum + ".</span> " : "";
            const nameHtml = item.pdf ? '<a href="' + item.pdf + '" target="_blank">' + item.name + "</a>" : "<span>" + item.name + "</span>";
            const typeBadge = '<span class="type-badge type-' + item.type + '">' + item.type + "</span>";
            const levelClass = item.level ? " level-" + item.level : "";
            const levelBadge = item.level ? '<span class="level' + levelClass + '">' + item.level + "</span>" : "";
            let db = "";
            if (item.dh) {
                db = item.duration_days + "d / " + item.dh + "h";
            }
            const durationBadge = db ? '<span class="duration">' + db + "</span>" : "";
            const chaptersBadge = item.chapters ? '<span class="chapters-badge">' + item.chapters + " ch</span>" : "";
            const slidesBadge = item.slides ? '<span class="slides-badge">' + item.slides + " sl</span>" : "";
            const pdfLink = item.pdf ? '<a class="dl-icon" href="' + item.pdf + '" download title="Download PDF">' + ICON_PDF + "</a>" : "";
            html += "<li>" + numPrefix + nameHtml + typeBadge + levelBadge + durationBadge + chaptersBadge + slidesBadge + " " + pdfLink + "</li>";
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
levelEl.addEventListener("change", render);
categoryEl.addEventListener("change", render);
typeEl.addEventListener("change", render);
tagEl.addEventListener("change", render);
audienceEl.addEventListener("change", render);
durationEl.addEventListener("change", render);
numbersEl.addEventListener("change", render);
sort1El.addEventListener("change", render);
sort1DirEl.addEventListener("change", render);
sort2El.addEventListener("change", render);
sort2DirEl.addEventListener("change", render);

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

// Theme switcher (shared from shared-themes/theme-switcher.js)
initThemeSwitcher({ storageKey: "course-browser-theme", defaultTheme: "paper" });
