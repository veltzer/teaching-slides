# Chapter 2: Android UI Architecture
## Advanced View Development and Layout Systems

---

## View Architecture Overview

![0](../../../out/mermaid/marp/courses/advanced-android-application-development/chapter2.md/0.png)

---

## ConstraintLayout Advanced Features

```xml
<androidx.constraintlayout.widget.ConstraintLayout
    android:layout_width="match_parent"
    android:layout_height="match_parent">

    <ImageView
        android:id="@+id/profile_image"
        android:layout_width="0dp"
        android:layout_height="0dp"
        app:layout_constraintDimensionRatio="1:1"
        app:layout_constraintWidth_percent="0.4"
        app:layout_constraintTop_toTopOf="parent"
        app:layout_constraintStart_toStartOf="parent"/>

    <TextView
        android:layout_width="0dp"
        android:layout_height="wrap_content"
        app:layout_constraintStart_toEndOf="@id/profile_image"
        app:layout_constraintTop_toTopOf="@id/profile_image"
        app:layout_constraintEnd_toEndOf="parent"
        app:layout_constraintHorizontal_bias="0.3"/>

</androidx.constraintlayout.widget.ConstraintLayout>
```

---

## Custom View Lifecycle

![1](../../../out/mermaid/marp/courses/advanced-android-application-development/chapter2.md/1.png)

---

## Custom View Implementation

```java
public class CircularProgressView extends View {
    private Paint paint;
    private float progress;

    public CircularProgressView(Context context, AttributeSet attrs) {
        super(context, attrs);
        init(attrs);
    }

    private void init(AttributeSet attrs) {
        paint = new Paint(Paint.ANTI_ALIAS_FLAG);
        // Read custom attributes
        TypedArray a = getContext().obtainStyledAttributes(
            attrs,
            R.styleable.CircularProgressView
        );
        // Use attributes
        a.recycle();
    }

    @Override
    protected void onDraw(Canvas canvas) {
        super.onDraw(canvas);
        // Draw custom view
        float centerX = getWidth() / 2f;
        float centerY = getHeight() / 2f;
        canvas.drawCircle(centerX, centerY, radius, paint);
    }
}
```

---

## Custom Attributes

```xml
<!-- attrs.xml -->
<declare-styleable name="CircularProgressView">
    <attr name="progressColor" format="color"/>
    <attr name="strokeWidth" format="dimension"/>
    <attr name="maxProgress" format="integer"/>
</declare-styleable>

<!-- Layout usage -->
<com.example.CircularProgressView
    android:layout_width="100dp"
    android:layout_height="100dp"
    app:progressColor="@color/blue"
    app:strokeWidth="4dp"
    app:maxProgress="100"/>
```

---

## View Binding Implementation

```java
public class ProfileActivity extends AppCompatActivity {
    private ActivityProfileBinding binding;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        binding = ActivityProfileBinding.inflate(getLayoutInflater());
        setContentView(binding.getRoot());

        // Use view binding
        binding.usernameText.setText("John Doe");
        binding.profileImage.setImageResource(R.drawable.profile);
        binding.saveButton.setOnClickListener(v -> saveProfile());
    }

    @Override
    protected void onDestroy() {
        super.onDestroy();
        binding = null;
    }
}
```

---

## Fragment Lifecycle

![2](../../../out/mermaid/marp/courses/advanced-android-application-development/chapter2.md/2.png)

---

## Fragment Implementation

```java
public class ProfileFragment extends Fragment {
    private FragmentProfileBinding binding;

    @Override
    public View onCreateView(
            LayoutInflater inflater,
            ViewGroup container,
            Bundle savedInstanceState) {
        binding = FragmentProfileBinding.inflate(
            inflater,
            container,
            false
        );
        return binding.getRoot();
    }

    @Override
    public void onViewCreated(View view, Bundle savedInstanceState) {
        super.onViewCreated(view, savedInstanceState);
        setupUI();
        observeViewModel();
    }

    @Override
    public void onDestroyView() {
        super.onDestroyView();
        binding = null;
    }
}
```

---

## Custom ViewGroup Example

```java
public class FlowLayout extends ViewGroup {
    @Override
    protected void onMeasure(int widthMeasureSpec, int heightMeasureSpec) {
        int width = MeasureSpec.getSize(widthMeasureSpec);
        int height = 0;
        int lineHeight = 0;
        int xPos = 0;

        for (int i = 0; i < getChildCount(); i++) {
            View child = getChildAt(i);
            measureChild(child, widthMeasureSpec, heightMeasureSpec);

            if (xPos + child.getMeasuredWidth() > width) {
                height += lineHeight;
                xPos = 0;
                lineHeight = child.getMeasuredHeight();
            } else {
                lineHeight = Math.max(
                    lineHeight,
                    child.getMeasuredHeight()
                );
            }
            xPos += child.getMeasuredWidth();
        }
        height += lineHeight;
        setMeasuredDimension(width, height);
    }

    @Override
    protected void onLayout(boolean changed, int l, int t, int r, int b) {
        // Implement layout logic
    }
}
```

---

## Performance Optimization

| Technique | Implementation | Benefit |
|-----------|---------------|----------|
| View Flattening | Merge layouts | Reduces hierarchy |
| ViewStub | Lazy loading | Memory efficient |
| RecyclerView | View recycling | Smooth scrolling |
| Hardware acceleration | Layer-type | Better rendering |

---

## Layout Inspector

![3](../../../out/mermaid/marp/courses/advanced-android-application-development/chapter2.md/3.png)

---

## Best Practices

![4](../../../out/mermaid/marp/courses/advanced-android-application-development/chapter2.md/4.png)

---

## Assignment Preview
### Custom UI Components

Create an application that demonstrates:
1. Custom View implementation
1. Custom ViewGroup implementation
1. Complex ConstraintLayout
1. ViewBinding usage
1. Fragment navigation
1. Performance optimization

---

## Resources

- Android UI Documentation
- Custom View Guide
- ViewBinding Documentation
- Layout Optimization Guide
- Sample Code Repository
