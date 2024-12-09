# Chapter 3: Material Design and Animations
## Creating Engaging User Interfaces

---

# Material Design Principles

![0](../../../out/mermaid/marp/courses/advanced-android-application-development/chapter3.md/0.png)

---

# Theme Implementation

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

# Material Components

| Component | Usage | Key Attributes |
|-----------|-------|----------------|
| MaterialButton | Interactive buttons | `app:cornerRadius`, `app:icon` |
| TextInputLayout | Text input fields | `app:errorEnabled`, `app:helperText` |
| Card | Content containers | `app:cardElevation`, `app:cardCornerRadius` |
| BottomNavigation | Navigation | `app:menu`, `app:labelVisibilityMode` |

---

# Custom Themes and Styles

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

# Typography System

![1](../../../out/mermaid/marp/courses/advanced-android-application-development/chapter3.md/1.png)

---

# Animation Types in Android

![2](../../../out/mermaid/marp/courses/advanced-android-application-development/chapter3.md/2.png)

---

# Property Animation Example

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

# Motion Layout Basics

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

# Transition Framework

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

# Custom View Animation

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

# Material Design Components in Practice

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

# Best Practices

![3](../../../out/mermaid/marp/courses/advanced-android-application-development/chapter3.md/3.png)

---

# Assignment Preview
## Material Design Implementation

Create an app screen that demonstrates:
- Custom theme implementation
- Complex animations
- Material components usage
- Motion Layout transitions
- Responsive layout design

Due: End of Chapter 3

---

# Resources

- Material Design Guidelines
- Android Animation Documentation
- MotionLayout Code Lab
- Material Components Repository
- Animation Samples Repository
