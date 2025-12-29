# Material Design and Animations
## Creating Engaging User Interfaces

---

## Material Design Principles

<svg width="600" height="400" xmlns="http://www.w3.org/2000/svg">
  <!-- Central Material Design node -->
  <ellipse cx="300" cy="200" rx="80" ry="40" fill="#673ab7" stroke="#333" stroke-width="3"/>
  <text x="300" y="200" text-anchor="middle" font-size="14" fill="white" font-weight="bold">Material</text>
  <text x="300" y="218" text-anchor="middle" font-size="14" fill="white" font-weight="bold">Design</text>

  <!-- Surface branch -->
  <ellipse cx="150" cy="100" rx="50" ry="30" fill="#e3f2fd" stroke="#333" stroke-width="2"/>
  <text x="150" y="105" text-anchor="middle" font-size="12" font-weight="bold">Surface</text>

  <!-- Color branch -->
  <ellipse cx="450" cy="100" rx="50" ry="30" fill="#f3e5f5" stroke="#333" stroke-width="2"/>
  <text x="450" y="105" text-anchor="middle" font-size="12" font-weight="bold">Color</text>

  <!-- Typography branch -->
  <ellipse cx="150" cy="300" rx="60" ry="30" fill="#e8f5e9" stroke="#333" stroke-width="2"/>
  <text x="150" y="305" text-anchor="middle" font-size="12" font-weight="bold">Typography</text>

  <!-- Motion branch -->
  <ellipse cx="450" cy="300" rx="50" ry="30" fill="#fff3e0" stroke="#333" stroke-width="2"/>
  <text x="450" y="305" text-anchor="middle" font-size="12" font-weight="bold">Motion</text>

  <!-- Surface sub-elements -->
  <rect x="30" y="40" width="70" height="25" fill="#e1f5fe" stroke="#333" stroke-width="1" rx="5"/>
  <text x="65" y="57" text-anchor="middle" font-size="10">Elevation</text>

  <rect x="30" y="75" width="70" height="25" fill="#e1f5fe" stroke="#333" stroke-width="1" rx="5"/>
  <text x="65" y="92" text-anchor="middle" font-size="10">Shadow</text>

  <rect x="30" y="110" width="70" height="25" fill="#e1f5fe" stroke="#333" stroke-width="1" rx="5"/>
  <text x="65" y="127" text-anchor="middle" font-size="10">Shape</text>

  <!-- Color sub-elements -->
  <rect x="500" y="30" width="70" height="25" fill="#fce4ec" stroke="#333" stroke-width="1" rx="5"/>
  <text x="535" y="47" text-anchor="middle" font-size="10">Primary</text>

  <rect x="500" y="60" width="70" height="25" fill="#fce4ec" stroke="#333" stroke-width="1" rx="5"/>
  <text x="535" y="77" text-anchor="middle" font-size="10">Secondary</text>

  <rect x="500" y="90" width="70" height="25" fill="#fce4ec" stroke="#333" stroke-width="1" rx="5"/>
  <text x="535" y="107" text-anchor="middle" font-size="10">Surface</text>

  <rect x="500" y="120" width="70" height="25" fill="#fce4ec" stroke="#333" stroke-width="1" rx="5"/>
  <text x="535" y="137" text-anchor="middle" font-size="10">Error</text>

  <!-- Typography sub-elements -->
  <rect x="30" y="270" width="70" height="25" fill="#c8e6c9" stroke="#333" stroke-width="1" rx="5"/>
  <text x="65" y="287" text-anchor="middle" font-size="10">Scale</text>

  <rect x="30" y="300" width="70" height="25" fill="#c8e6c9" stroke="#333" stroke-width="1" rx="5"/>
  <text x="65" y="317" text-anchor="middle" font-size="10">Hierarchy</text>

  <rect x="30" y="330" width="70" height="25" fill="#c8e6c9" stroke="#333" stroke-width="1" rx="5"/>
  <text x="65" y="347" text-anchor="middle" font-size="10">Readability</text>

  <!-- Motion sub-elements -->
  <rect x="500" y="270" width="70" height="25" fill="#ffe0b2" stroke="#333" stroke-width="1" rx="5"/>
  <text x="535" y="287" text-anchor="middle" font-size="10">Natural</text>

  <rect x="500" y="300" width="70" height="25" fill="#ffe0b2" stroke="#333" stroke-width="1" rx="5"/>
  <text x="535" y="317" text-anchor="middle" font-size="10">Meaningful</text>

  <rect x="500" y="330" width="70" height="25" fill="#ffe0b2" stroke="#333" stroke-width="1" rx="5"/>
  <text x="535" y="347" text-anchor="middle" font-size="10">Responsive</text>

  <!-- Connection lines -->
  <line x1="240" y1="180" x2="190" y2="120" stroke="#333" stroke-width="2"/>
  <line x1="360" y1="180" x2="410" y2="120" stroke="#333" stroke-width="2"/>
  <line x1="240" y1="220" x2="190" y2="280" stroke="#333" stroke-width="2"/>
  <line x1="360" y1="220" x2="410" y2="280" stroke="#333" stroke-width="2"/>

  <!-- Sub-connections -->
  <line x1="100" y1="90" x2="100" y2="52" stroke="#666" stroke-width="1"/>
  <line x1="100" y1="100" x2="100" y2="87" stroke="#666" stroke-width="1"/>
  <line x1="100" y1="110" x2="100" y2="122" stroke="#666" stroke-width="1"/>

  <line x1="500" y1="90" x2="500" y2="42" stroke="#666" stroke-width="1"/>
  <line x1="500" y1="100" x2="500" y2="72" stroke="#666" stroke-width="1"/>
  <line x1="500" y1="110" x2="500" y2="102" stroke="#666" stroke-width="1"/>
  <line x1="500" y1="120" x2="500" y2="132" stroke="#666" stroke-width="1"/>

  <line x1="100" y1="295" x2="100" y2="282" stroke="#666" stroke-width="1"/>
  <line x1="100" y1="305" x2="100" y2="312" stroke="#666" stroke-width="1"/>
  <line x1="100" y1="315" x2="100" y2="342" stroke="#666" stroke-width="1"/>

  <line x1="500" y1="295" x2="500" y2="282" stroke="#666" stroke-width="1"/>
  <line x1="500" y1="305" x2="500" y2="312" stroke="#666" stroke-width="1"/>
  <line x1="500" y1="315" x2="500" y2="342" stroke="#666" stroke-width="1"/>
</svg>

---

## Theme Implementation

```xml
<!-- styles.xml -->
<style name="AppTheme" parent="Theme.MaterialComponents.Light.NoActionBar">
    <!-- Primary brand color -->
    <item name="colorPrimary">@color/purple_500</item>
    <item name="colorPrimaryVariant">@color/purple_700</item>
    <item name="colorOnPrimary">@color/white</item>

    <!-- Secondary brand color -->
    <item name="colorSecondary">@color/teal_200</item>
    <item name="colorSecondaryVariant">@color/teal_700</item>
    <item name="colorOnSecondary">@color/black</item>

    <!-- Status bar color -->
    <item name="android:statusBarColor">?attr/colorPrimaryVariant</item>
</style>
```

---

## Material Components

| Component | Usage | Key Attributes |
|-----------|-------|----------------|
| MaterialButton | Interactive buttons | `app:cornerRadius`, `app:icon` |
| TextInputLayout | Text input fields | `app:errorEnabled`, `app:helperText` |
| Card | Content containers | `app:cardElevation`, `app:cardCornerRadius` |
| BottomNavigation | Navigation | `app:menu`, `app:labelVisibilityMode` |

---

## Custom Themes and Styles

```xml
<!-- Custom button style -->
<style name="CustomButton" parent="Widget.MaterialComponents.Button">
    <item name="android:textSize">16sp</item>
    <item name="cornerRadius">8dp</item>
    <item name="android:paddingStart">24dp</item>
    <item name="android:paddingEnd">24dp</item>
    <item name="android:letterSpacing">0.025</item>
</style>
```

---

## Typography System

<svg width="600" height="350" xmlns="http://www.w3.org/2000/svg">
  <!-- Typography Scale root -->
  <rect x="225" y="30" width="150" height="50" fill="#673ab7" stroke="#333" stroke-width="2" rx="5"/>
  <text x="300" y="60" text-anchor="middle" font-size="14" fill="white" font-weight="bold">Typography Scale</text>

  <!-- Main categories -->
  <rect x="50" y="130" width="100" height="40" fill="#e3f2fd" stroke="#333" stroke-width="2" rx="5"/>
  <text x="100" y="155" text-anchor="middle" font-size="12">Headlines</text>

  <rect x="180" y="130" width="100" height="40" fill="#f3e5f5" stroke="#333" stroke-width="2" rx="5"/>
  <text x="230" y="155" text-anchor="middle" font-size="12">Subtitles</text>

  <rect x="310" y="130" width="100" height="40" fill="#e8f5e9" stroke="#333" stroke-width="2" rx="5"/>
  <text x="360" y="155" text-anchor="middle" font-size="12">Body</text>

  <rect x="440" y="130" width="100" height="40" fill="#fff3e0" stroke="#333" stroke-width="2" rx="5"/>
  <text x="490" y="155" text-anchor="middle" font-size="12">Caption</text>

  <!-- Headlines sub-items -->
  <rect x="20" y="220" width="50" height="30" fill="#e1f5fe" stroke="#333" stroke-width="1" rx="5"/>
  <text x="45" y="240" text-anchor="middle" font-size="11">H1</text>

  <rect x="75" y="220" width="50" height="30" fill="#e1f5fe" stroke="#333" stroke-width="1" rx="5"/>
  <text x="100" y="240" text-anchor="middle" font-size="11">H2</text>

  <rect x="130" y="220" width="50" height="30" fill="#e1f5fe" stroke="#333" stroke-width="1" rx="5"/>
  <text x="155" y="240" text-anchor="middle" font-size="11">H3</text>

  <!-- Body sub-items -->
  <rect x="285" y="220" width="60" height="30" fill="#c8e6c9" stroke="#333" stroke-width="1" rx="5"/>
  <text x="315" y="240" text-anchor="middle" font-size="11">Body 1</text>

  <rect x="350" y="220" width="60" height="30" fill="#c8e6c9" stroke="#333" stroke-width="1" rx="5"/>
  <text x="380" y="240" text-anchor="middle" font-size="11">Body 2</text>

  <!-- Arrows from root to categories -->
  <line x1="260" y1="80" x2="100" y2="130" stroke="#333" stroke-width="2" marker-end="url(#arrow_typo)"/>
  <line x1="280" y1="80" x2="230" y2="130" stroke="#333" stroke-width="2" marker-end="url(#arrow_typo)"/>
  <line x1="320" y1="80" x2="360" y2="130" stroke="#333" stroke-width="2" marker-end="url(#arrow_typo)"/>
  <line x1="340" y1="80" x2="490" y2="130" stroke="#333" stroke-width="2" marker-end="url(#arrow_typo)"/>

  <!-- Arrows to sub-items -->
  <line x1="80" y1="170" x2="45" y2="220" stroke="#333" stroke-width="2" marker-end="url(#arrow_typo)"/>
  <line x1="100" y1="170" x2="100" y2="220" stroke="#333" stroke-width="2" marker-end="url(#arrow_typo)"/>
  <line x1="120" y1="170" x2="155" y2="220" stroke="#333" stroke-width="2" marker-end="url(#arrow_typo)"/>

  <line x1="340" y1="170" x2="315" y2="220" stroke="#333" stroke-width="2" marker-end="url(#arrow_typo)"/>
  <line x1="380" y1="170" x2="380" y2="220" stroke="#333" stroke-width="2" marker-end="url(#arrow_typo)"/>

  <defs>
    <marker id="arrow_typo" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <path d="M0,0 L0,6 L9,3 z" fill="#333"/>
    </marker>
  </defs>
</svg>

---

## Animation Types in Android

<svg width="600" height="300" xmlns="http://www.w3.org/2000/svg">
  <!-- Android Animations root -->
  <rect x="200" y="30" width="200" height="50" fill="#4caf50" stroke="#333" stroke-width="2" rx="5"/>
  <text x="300" y="60" text-anchor="middle" font-size="14" fill="white" font-weight="bold">Android Animations</text>

  <!-- Three main branches -->
  <rect x="50" y="130" width="140" height="40" fill="#e3f2fd" stroke="#333" stroke-width="2" rx="5"/>
  <text x="120" y="155" text-anchor="middle" font-size="12">Property Animation</text>

  <rect x="230" y="130" width="120" height="40" fill="#f3e5f5" stroke="#333" stroke-width="2" rx="5"/>
  <text x="290" y="155" text-anchor="middle" font-size="12">View Animation</text>

  <rect x="390" y="130" width="150" height="40" fill="#e8f5e9" stroke="#333" stroke-width="2" rx="5"/>
  <text x="465" y="155" text-anchor="middle" font-size="12">Transition Animation</text>

  <!-- Property Animation sub-items -->
  <rect x="20" y="220" width="100" height="30" fill="#e1f5fe" stroke="#333" stroke-width="1" rx="5"/>
  <text x="70" y="240" text-anchor="middle" font-size="11">ValueAnimator</text>

  <rect x="130" y="220" width="100" height="30" fill="#e1f5fe" stroke="#333" stroke-width="1" rx="5"/>
  <text x="180" y="240" text-anchor="middle" font-size="11">ObjectAnimator</text>

  <!-- View Animation sub-items -->
  <rect x="210" y="220" width="110" height="30" fill="#fce4ec" stroke="#333" stroke-width="1" rx="5"/>
  <text x="265" y="240" text-anchor="middle" font-size="11">Tween Animation</text>

  <rect x="330" y="220" width="110" height="30" fill="#fce4ec" stroke="#333" stroke-width="1" rx="5"/>
  <text x="385" y="240" text-anchor="middle" font-size="11">Frame Animation</text>

  <!-- Arrows from root to main branches -->
  <line x1="250" y1="80" x2="120" y2="130" stroke="#333" stroke-width="2" marker-end="url(#arrow_anim)"/>
  <line x1="300" y1="80" x2="290" y2="130" stroke="#333" stroke-width="2" marker-end="url(#arrow_anim)"/>
  <line x1="350" y1="80" x2="465" y2="130" stroke="#333" stroke-width="2" marker-end="url(#arrow_anim)"/>

  <!-- Arrows to sub-items -->
  <line x1="100" y1="170" x2="70" y2="220" stroke="#333" stroke-width="2" marker-end="url(#arrow_anim)"/>
  <line x1="140" y1="170" x2="180" y2="220" stroke="#333" stroke-width="2" marker-end="url(#arrow_anim)"/>

  <line x1="270" y1="170" x2="265" y2="220" stroke="#333" stroke-width="2" marker-end="url(#arrow_anim)"/>
  <line x1="310" y1="170" x2="385" y2="220" stroke="#333" stroke-width="2" marker-end="url(#arrow_anim)"/>

  <defs>
    <marker id="arrow_anim" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <path d="M0,0 L0,6 L9,3 z" fill="#333"/>
    </marker>
  </defs>
</svg>

---

## Property Animation Example

```java
public class AnimationDemo extends AppCompatActivity {
    private void animateButton(Button button) {
        ObjectAnimator scaleX = ObjectAnimator.ofFloat(
            button, "scaleX", 1f, 1.2f, 1f
        );
        ObjectAnimator scaleY = ObjectAnimator.ofFloat(
            button, "scaleY", 1f, 1.2f, 1f
        );

        AnimatorSet set = new AnimatorSet();
        set.playTogether(scaleX, scaleY);
        set.setDuration(300);
        set.setInterpolator(new OvershootInterpolator());
        set.start();
    }
}
```

---

## Motion Layout Basics

```xml
<!-- motion_scene.xml -->
<MotionScene xmlns:android="..."
    xmlns:motion="...">

    <Transition
        motion:constraintSetStart="@+id/start"
        motion:constraintSetEnd="@+id/end">
        <OnSwipe
            motion:dragDirection="dragUp"
            motion:touchAnchorId="@id/button" />
    </Transition>

    <ConstraintSet android:id="@+id/start">
        <!-- Start constraints -->
    </ConstraintSet>

    <ConstraintSet android:id="@+id/end">
        <!-- End constraints -->
    </ConstraintSet>
</MotionScene>
```

---

## Transition Framework

```java
public class TransitionDemo extends AppCompatActivity {
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_transition);

        // Set up transition
        TransitionManager.beginDelayedTransition(
            container,
            new AutoTransition()
        );

        // Change visibility or layout params to trigger transition
        detailsView.setVisibility(
            detailsView.getVisibility() == View.GONE
                ? View.VISIBLE
                : View.GONE
        );
    }
}
```

---

## Custom View Animation

```java
public class PulseAnimation extends Animation {
    private float mStartScale;
    private float mEndScale;
    private View mView;

    @Override
    protected void applyTransformation(
            float interpolatedTime,
            Transformation t) {
        float scale = mStartScale + (mEndScale - mStartScale)
            * interpolatedTime;
        mView.setScaleX(scale);
        mView.setScaleY(scale);
    }
}
```

---

## Material Design Components in Practice

```xml
<com.google.android.material.card.MaterialCardView
    android:layout_width="match_parent"
    android:layout_height="wrap_content"
    android:layout_margin="16dp"
    app:cardElevation="4dp"
    app:cardCornerRadius="8dp">

    <com.google.android.material.textfield.TextInputLayout
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:layout_margin="16dp"
        app:errorEnabled="true"
        style="@style/Widget.MaterialComponents.TextInputLayout.OutlinedBox">

        <com.google.android.material.textfield.TextInputEditText
            android:layout_width="match_parent"
            android:layout_height="wrap_content"
            android:hint="Enter text"/>

    </com.google.android.material.textfield.TextInputLayout>
</com.google.android.material.card.MaterialCardView>
```

---

## Best Practices

<svg width="600" height="350" xmlns="http://www.w3.org/2000/svg">
  <!-- Material Design Best Practices flow -->
  <rect x="150" y="30" width="300" height="40" fill="#673ab7" stroke="#333" stroke-width="2" rx="5"/>
  <text x="300" y="55" text-anchor="middle" font-size="14" fill="white" font-weight="bold">Material Design Best Practices</text>

  <!-- Best practices items in sequence -->
  <rect x="200" y="100" width="200" height="35" fill="#e3f2fd" stroke="#333" stroke-width="2" rx="5"/>
  <text x="300" y="122" text-anchor="middle" font-size="12">Consistent Spacing</text>

  <rect x="200" y="150" width="200" height="35" fill="#f3e5f5" stroke="#333" stroke-width="2" rx="5"/>
  <text x="300" y="172" text-anchor="middle" font-size="12">Color Hierarchy</text>

  <rect x="200" y="200" width="200" height="35" fill="#e8f5e9" stroke="#333" stroke-width="2" rx="5"/>
  <text x="300" y="222" text-anchor="middle" font-size="12">Typography Scale</text>

  <rect x="200" y="250" width="200" height="35" fill="#fff3e0" stroke="#333" stroke-width="2" rx="5"/>
  <text x="300" y="272" text-anchor="middle" font-size="12">Meaningful Motion</text>

  <rect x="200" y="300" width="200" height="35" fill="#fce4ec" stroke="#333" stroke-width="2" rx="5"/>
  <text x="300" y="322" text-anchor="middle" font-size="12">Accessibility</text>

  <rect x="400" y="300" width="200" height="35" fill="#e1f5fe" stroke="#333" stroke-width="2" rx="5"/>
  <text x="500" y="322" text-anchor="middle" font-size="12">Dark Theme Support</text>

  <!-- Flow arrows -->
  <line x1="300" y1="70" x2="300" y2="100" stroke="#333" stroke-width="2" marker-end="url(#arrow_bp)"/>
  <line x1="300" y1="135" x2="300" y2="150" stroke="#333" stroke-width="2" marker-end="url(#arrow_bp)"/>
  <line x1="300" y1="185" x2="300" y2="200" stroke="#333" stroke-width="2" marker-end="url(#arrow_bp)"/>
  <line x1="300" y1="235" x2="300" y2="250" stroke="#333" stroke-width="2" marker-end="url(#arrow_bp)"/>
  <line x1="300" y1="285" x2="300" y2="300" stroke="#333" stroke-width="2" marker-end="url(#arrow_bp)"/>
  <line x1="400" y1="317" x2="400" y2="317" stroke="#333" stroke-width="2" marker-end="url(#arrow_bp)"/>

  <defs>
    <marker id="arrow_bp" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <path d="M0,0 L0,6 L9,3 z" fill="#333"/>
    </marker>
  </defs>
</svg>

---

## Assignment Preview
### Material Design Implementation

Create an app screen that demonstrates:
- Custom theme implementation
- Complex animations
- Material components usage
- Motion Layout transitions
- Responsive layout design

---

## Resources

- Material Design Guidelines
- Android Animation Documentation
- MotionLayout Code Lab
- Material Components Repository
- Animation Samples Repository
