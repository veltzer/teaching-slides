# Android UI Architecture
## Advanced View Development and Layout Systems

---

## View Architecture Overview

<svg width="600" height="350" xmlns="http://www.w3.org/2000/svg">
  <!-- Main View class -->
  <rect x="250" y="30" width="100" height="50" fill="#e3f2fd" stroke="#333" stroke-width="2" rx="5"/>
  <text x="300" y="60" text-anchor="middle" font-size="14" font-weight="bold">View</text>

  <!-- ViewGroup extending View -->
  <rect x="250" y="130" width="100" height="50" fill="#f3e5f5" stroke="#333" stroke-width="2" rx="5"/>
  <text x="300" y="160" text-anchor="middle" font-size="14" font-weight="bold">ViewGroup</text>

  <!-- ViewGroup subclasses -->
  <rect x="50" y="230" width="100" height="40" fill="#e8f5e9" stroke="#333" stroke-width="2" rx="5"/>
  <text x="100" y="255" text-anchor="middle" font-size="12">LinearLayout</text>

  <rect x="180" y="230" width="110" height="40" fill="#e8f5e9" stroke="#333" stroke-width="2" rx="5"/>
  <text x="235" y="255" text-anchor="middle" font-size="12">ConstraintLayout</text>

  <rect x="320" y="230" width="100" height="40" fill="#e8f5e9" stroke="#333" stroke-width="2" rx="5"/>
  <text x="370" y="255" text-anchor="middle" font-size="12">FrameLayout</text>

  <rect x="450" y="230" width="120" height="40" fill="#e8f5e9" stroke="#333" stroke-width="2" rx="5"/>
  <text x="510" y="255" text-anchor="middle" font-size="11">Custom ViewGroup</text>

  <!-- Direct View subclasses -->
  <rect x="50" y="300" width="80" height="35" fill="#fff3e0" stroke="#333" stroke-width="2" rx="5"/>
  <text x="90" y="322" text-anchor="middle" font-size="12">TextView</text>

  <rect x="150" y="300" width="85" height="35" fill="#fff3e0" stroke="#333" stroke-width="2" rx="5"/>
  <text x="192" y="322" text-anchor="middle" font-size="12">ImageView</text>

  <rect x="255" y="300" width="80" height="35" fill="#fff3e0" stroke="#333" stroke-width="2" rx="5"/>
  <text x="295" y="322" text-anchor="middle" font-size="12">Button</text>

  <rect x="355" y="300" width="95" height="35" fill="#fff3e0" stroke="#333" stroke-width="2" rx="5"/>
  <text x="402" y="322" text-anchor="middle" font-size="12">Custom View</text>

  <!-- Inheritance arrows -->
  <line x1="300" y1="80" x2="300" y2="130" stroke="#333" stroke-width="2" marker-end="url(#arrow1)"/>

  <!-- ViewGroup to subclasses -->
  <line x1="280" y1="180" x2="100" y2="230" stroke="#333" stroke-width="2" marker-end="url(#arrow1)"/>
  <line x1="290" y1="180" x2="235" y2="230" stroke="#333" stroke-width="2" marker-end="url(#arrow1)"/>
  <line x1="310" y1="180" x2="370" y2="230" stroke="#333" stroke-width="2" marker-end="url(#arrow1)"/>
  <line x1="320" y1="180" x2="510" y2="230" stroke="#333" stroke-width="2" marker-end="url(#arrow1)"/>

  <!-- View to direct subclasses -->
  <line x1="270" y1="80" x2="90" y2="300" stroke="#333" stroke-width="2" marker-end="url(#arrow1)"/>
  <line x1="280" y1="80" x2="192" y2="300" stroke="#333" stroke-width="2" marker-end="url(#arrow1)"/>
  <line x1="295" y1="80" x2="295" y2="300" stroke="#333" stroke-width="2" marker-end="url(#arrow1)"/>
  <line x1="320" y1="80" x2="402" y2="300" stroke="#333" stroke-width="2" marker-end="url(#arrow1)"/>

  <defs>
    <marker id="arrow1" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <path d="M0,0 L0,6 L9,3 z" fill="#333"/>
    </marker>
  </defs>
</svg>

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

<svg width="600" height="350" xmlns="http://www.w3.org/2000/svg">
  <!-- Constructor -->
  <rect x="250" y="30" width="100" height="40" fill="#e3f2fd" stroke="#333" stroke-width="2" rx="5"/>
  <text x="300" y="55" text-anchor="middle" font-size="12">Constructor</text>

  <!-- onAttachedToWindow -->
  <rect x="220" y="100" width="160" height="40" fill="#f3e5f5" stroke="#333" stroke-width="2" rx="5"/>
  <text x="300" y="125" text-anchor="middle" font-size="12">onAttachedToWindow</text>

  <!-- onMeasure -->
  <rect x="250" y="170" width="100" height="40" fill="#e8f5e9" stroke="#333" stroke-width="2" rx="5"/>
  <text x="300" y="195" text-anchor="middle" font-size="12">onMeasure</text>

  <!-- onLayout -->
  <rect x="250" y="240" width="100" height="40" fill="#fff3e0" stroke="#333" stroke-width="2" rx="5"/>
  <text x="300" y="265" text-anchor="middle" font-size="12">onLayout</text>

  <!-- onDraw -->
  <rect x="450" y="170" width="100" height="40" fill="#fce4ec" stroke="#333" stroke-width="2" rx="5"/>
  <text x="500" y="195" text-anchor="middle" font-size="12">onDraw</text>

  <!-- onDetachedFromWindow -->
  <rect x="200" y="310" width="200" height="40" fill="#ffebee" stroke="#333" stroke-width="2" rx="5"/>
  <text x="300" y="335" text-anchor="middle" font-size="12">onDetachedFromWindow</text>

  <!-- Flow arrows -->
  <line x1="300" y1="70" x2="300" y2="100" stroke="#333" stroke-width="2" marker-end="url(#arrow2)"/>
  <line x1="300" y1="140" x2="300" y2="170" stroke="#333" stroke-width="2" marker-end="url(#arrow2)"/>
  <line x1="300" y1="210" x2="300" y2="240" stroke="#333" stroke-width="2" marker-end="url(#arrow2)"/>
  <line x1="350" y1="190" x2="450" y2="190" stroke="#333" stroke-width="2" marker-end="url(#arrow2)"/>
  <line x1="300" y1="280" x2="300" y2="310" stroke="#333" stroke-width="2" marker-end="url(#arrow2)"/>

  <!-- Loop backs -->
  <path d="M 270 170 Q 220 150, 220 190 Q 220 210, 270 210" stroke="#666" stroke-width="2" fill="none" stroke-dasharray="5,5" marker-end="url(#arrow2)"/>
  <text x="180" y="195" font-size="10" fill="#666">repeat</text>

  <path d="M 530 170 Q 560 150, 560 190 Q 560 210, 530 210" stroke="#666" stroke-width="2" fill="none" stroke-dasharray="5,5" marker-end="url(#arrow2)"/>
  <text x="575" y="195" font-size="10" fill="#666">repeat</text>

  <defs>
    <marker id="arrow2" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <path d="M0,0 L0,6 L9,3 z" fill="#333"/>
    </marker>
  </defs>
</svg>

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

<svg width="600" height="400" xmlns="http://www.w3.org/2000/svg">
  <!-- Initial state -->
  <circle cx="50" cy="50" r="20" fill="#333" stroke="#333" stroke-width="2"/>

  <!-- onAttach -->
  <rect x="120" y="35" width="80" height="30" fill="#e3f2fd" stroke="#333" stroke-width="2" rx="15"/>
  <text x="160" y="55" text-anchor="middle" font-size="11">onAttach</text>

  <!-- onCreate -->
  <rect x="230" y="35" width="80" height="30" fill="#f3e5f5" stroke="#333" stroke-width="2" rx="15"/>
  <text x="270" y="55" text-anchor="middle" font-size="11">onCreate</text>

  <!-- onCreateView -->
  <rect x="340" y="35" width="100" height="30" fill="#e8f5e9" stroke="#333" stroke-width="2" rx="15"/>
  <text x="390" y="55" text-anchor="middle" font-size="11">onCreateView</text>

  <!-- onViewCreated -->
  <rect x="470" y="35" width="110" height="30" fill="#fff3e0" stroke="#333" stroke-width="2" rx="15"/>
  <text x="525" y="55" text-anchor="middle" font-size="11">onViewCreated</text>

  <!-- onStart -->
  <rect x="470" y="100" width="80" height="30" fill="#e1f5fe" stroke="#333" stroke-width="2" rx="15"/>
  <text x="510" y="120" text-anchor="middle" font-size="11">onStart</text>

  <!-- onResume -->
  <rect x="470" y="165" width="80" height="30" fill="#c8e6c9" stroke="#333" stroke-width="2" rx="15"/>
  <text x="510" y="185" text-anchor="middle" font-size="11">onResume</text>

  <!-- Active state indicator -->
  <rect x="450" y="220" width="120" height="40" fill="#4caf50" stroke="#333" stroke-width="3" rx="5"/>
  <text x="510" y="245" text-anchor="middle" font-size="12" fill="white" font-weight="bold">ACTIVE</text>

  <!-- onPause -->
  <rect x="340" y="295" width="80" height="30" fill="#ffccbc" stroke="#333" stroke-width="2" rx="15"/>
  <text x="380" y="315" text-anchor="middle" font-size="11">onPause</text>

  <!-- onStop -->
  <rect x="230" y="295" width="80" height="30" fill="#ffab91" stroke="#333" stroke-width="2" rx="15"/>
  <text x="270" y="315" text-anchor="middle" font-size="11">onStop</text>

  <!-- onDestroyView -->
  <rect x="100" y="295" width="110" height="30" fill="#ff8a65" stroke="#333" stroke-width="2" rx="15"/>
  <text x="155" y="315" text-anchor="middle" font-size="11">onDestroyView</text>

  <!-- onDestroy -->
  <rect x="120" y="350" width="80" height="30" fill="#ff7043" stroke="#333" stroke-width="2" rx="15"/>
  <text x="160" y="370" text-anchor="middle" font-size="11">onDestroy</text>

  <!-- onDetach -->
  <rect x="230" y="350" width="80" height="30" fill="#ff5722" stroke="#333" stroke-width="2" rx="15"/>
  <text x="270" y="370" text-anchor="middle" font-size="11">onDetach</text>

  <!-- Final state -->
  <circle cx="350" cy="365" r="20" fill="#333" stroke="#333" stroke-width="2"/>
  <circle cx="350" cy="365" r="15" fill="#fff"/>
  <circle cx="350" cy="365" r="10" fill="#333"/>

  <!-- Forward flow arrows -->
  <line x1="70" y1="50" x2="120" y2="50" stroke="#333" stroke-width="2" marker-end="url(#arrow3)"/>
  <line x1="200" y1="50" x2="230" y2="50" stroke="#333" stroke-width="2" marker-end="url(#arrow3)"/>
  <line x1="310" y1="50" x2="340" y2="50" stroke="#333" stroke-width="2" marker-end="url(#arrow3)"/>
  <line x1="440" y1="50" x2="470" y2="50" stroke="#333" stroke-width="2" marker-end="url(#arrow3)"/>
  <line x1="510" y1="65" x2="510" y2="100" stroke="#333" stroke-width="2" marker-end="url(#arrow3)"/>
  <line x1="510" y1="130" x2="510" y2="165" stroke="#333" stroke-width="2" marker-end="url(#arrow3)"/>
  <line x1="510" y1="195" x2="510" y2="220" stroke="#333" stroke-width="2" marker-end="url(#arrow3)"/>

  <!-- Reverse flow arrows -->
  <line x1="490" y1="260" x2="420" y2="295" stroke="#333" stroke-width="2" marker-end="url(#arrow3)"/>
  <line x1="340" y1="310" x2="310" y2="310" stroke="#333" stroke-width="2" marker-end="url(#arrow3)"/>
  <line x1="230" y1="310" x2="210" y2="310" stroke="#333" stroke-width="2" marker-end="url(#arrow3)"/>
  <line x1="155" y1="325" x2="160" y2="350" stroke="#333" stroke-width="2" marker-end="url(#arrow3)"/>
  <line x1="200" y1="365" x2="230" y2="365" stroke="#333" stroke-width="2" marker-end="url(#arrow3)"/>
  <line x1="310" y1="365" x2="330" y2="365" stroke="#333" stroke-width="2" marker-end="url(#arrow3)"/>

  <defs>
    <marker id="arrow3" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <path d="M0,0 L0,6 L9,3 z" fill="#333"/>
    </marker>
  </defs>
</svg>

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

<svg width="600" height="300" xmlns="http://www.w3.org/2000/svg">
  <!-- Main Layout Inspector -->
  <rect x="200" y="30" width="200" height="50" fill="#e3f2fd" stroke="#333" stroke-width="2" rx="5"/>
  <text x="300" y="60" text-anchor="middle" font-size="14" font-weight="bold">Layout Inspector</text>

  <!-- View Hierarchy branch -->
  <rect x="50" y="130" width="120" height="40" fill="#f3e5f5" stroke="#333" stroke-width="2" rx="5"/>
  <text x="110" y="155" text-anchor="middle" font-size="12">View Hierarchy</text>

  <!-- Performance Metrics branch -->
  <rect x="240" y="130" width="140" height="40" fill="#e8f5e9" stroke="#333" stroke-width="2" rx="5"/>
  <text x="310" y="155" text-anchor="middle" font-size="12">Performance Metrics</text>

  <!-- Layout Bounds branch -->
  <rect x="430" y="130" width="120" height="40" fill="#fff3e0" stroke="#333" stroke-width="2" rx="5"/>
  <text x="490" y="155" text-anchor="middle" font-size="12">Layout Bounds</text>

  <!-- 3D View -->
  <rect x="50" y="210" width="120" height="35" fill="#e1f5fe" stroke="#333" stroke-width="2" rx="5"/>
  <text x="110" y="232" text-anchor="middle" font-size="11">3D View</text>

  <!-- Rendering Stats -->
  <rect x="240" y="210" width="140" height="35" fill="#c8e6c9" stroke="#333" stroke-width="2" rx="5"/>
  <text x="310" y="232" text-anchor="middle" font-size="11">Rendering Stats</text>

  <!-- Overdraw -->
  <rect x="430" y="210" width="120" height="35" fill="#ffccbc" stroke="#333" stroke-width="2" rx="5"/>
  <text x="490" y="232" text-anchor="middle" font-size="11">Overdraw</text>

  <!-- Arrows from main to branches -->
  <line x1="250" y1="80" x2="110" y2="130" stroke="#333" stroke-width="2" marker-end="url(#arrow4)"/>
  <line x1="300" y1="80" x2="310" y2="130" stroke="#333" stroke-width="2" marker-end="url(#arrow4)"/>
  <line x1="350" y1="80" x2="490" y2="130" stroke="#333" stroke-width="2" marker-end="url(#arrow4)"/>

  <!-- Arrows from branches to sub-features -->
  <line x1="110" y1="170" x2="110" y2="210" stroke="#333" stroke-width="2" marker-end="url(#arrow4)"/>
  <line x1="310" y1="170" x2="310" y2="210" stroke="#333" stroke-width="2" marker-end="url(#arrow4)"/>
  <line x1="490" y1="170" x2="490" y2="210" stroke="#333" stroke-width="2" marker-end="url(#arrow4)"/>

  <defs>
    <marker id="arrow4" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <path d="M0,0 L0,6 L9,3 z" fill="#333"/>
    </marker>
  </defs>
</svg>

---

## Best Practices

<svg width="600" height="350" xmlns="http://www.w3.org/2000/svg">
  <!-- Center: UI Best Practices -->
  <ellipse cx="300" cy="175" rx="100" ry="50" fill="#e3f2fd" stroke="#333" stroke-width="2"/>
  <text x="300" y="175" text-anchor="middle" font-size="14" font-weight="bold">UI Best</text>
  <text x="300" y="195" text-anchor="middle" font-size="14" font-weight="bold">Practices</text>

  <!-- Layout Optimization branch -->
  <ellipse cx="120" cy="80" rx="85" ry="35" fill="#f3e5f5" stroke="#333" stroke-width="2"/>
  <text x="120" y="85" text-anchor="middle" font-size="12" font-weight="bold">Layout Optimization</text>

  <!-- Custom Views branch -->
  <ellipse cx="480" cy="80" rx="75" ry="35" fill="#e8f5e9" stroke="#333" stroke-width="2"/>
  <text x="480" y="85" text-anchor="middle" font-size="12" font-weight="bold">Custom Views</text>

  <!-- ViewBinding branch -->
  <ellipse cx="300" cy="300" rx="75" ry="35" fill="#fff3e0" stroke="#333" stroke-width="2"/>
  <text x="300" y="305" text-anchor="middle" font-size="12" font-weight="bold">ViewBinding</text>

  <!-- Layout Optimization sub-items -->
  <rect x="30" y="15" width="110" height="25" fill="#fce4ec" stroke="#333" stroke-width="1" rx="5"/>
  <text x="85" y="32" text-anchor="middle" font-size="10">Flatten Hierarchy</text>

  <rect x="10" y="120" width="100" height="25" fill="#fce4ec" stroke="#333" stroke-width="1" rx="5"/>
  <text x="60" y="137" text-anchor="middle" font-size="10">Avoid Overdraw</text>

  <rect x="130" y="120" width="120" height="25" fill="#fce4ec" stroke="#333" stroke-width="1" rx="5"/>
  <text x="190" y="137" text-anchor="middle" font-size="10">Use ConstraintLayout</text>

  <!-- Custom Views sub-items -->
  <rect x="410" y="15" width="100" height="25" fill="#c8e6c9" stroke="#333" stroke-width="1" rx="5"/>
  <text x="460" y="32" text-anchor="middle" font-size="10">Proper Lifecycle</text>

  <rect x="520" y="50" width="100" height="25" fill="#c8e6c9" stroke="#333" stroke-width="1" rx="5"/>
  <text x="570" y="67" text-anchor="middle" font-size="10">Efficient Drawing</text>

  <rect x="470" y="120" width="110" height="25" fill="#c8e6c9" stroke="#333" stroke-width="1" rx="5"/>
  <text x="525" y="137" text-anchor="middle" font-size="10">State Management</text>

  <!-- ViewBinding sub-items -->
  <rect x="180" y="330" width="80" height="25" fill="#ffe0b2" stroke="#333" stroke-width="1" rx="5"/>
  <text x="220" y="347" text-anchor="middle" font-size="10">Null Safety</text>

  <rect x="280" y="340" width="80" height="25" fill="#ffe0b2" stroke="#333" stroke-width="1" rx="5"/>
  <text x="320" y="357" text-anchor="middle" font-size="10">Type Safety</text>

  <rect x="380" y="330" width="85" height="25" fill="#ffe0b2" stroke="#333" stroke-width="1" rx="5"/>
  <text x="422" y="347" text-anchor="middle" font-size="10">Performance</text>

  <!-- Connection lines -->
  <line x1="220" y1="160" x2="120" y2="110" stroke="#333" stroke-width="2"/>
  <line x1="380" y1="160" x2="480" y2="110" stroke="#333" stroke-width="2"/>
  <line x1="300" y1="220" x2="300" y2="265" stroke="#333" stroke-width="2"/>

  <!-- Sub-connections -->
  <line x1="85" y1="50" x2="85" y2="40" stroke="#666" stroke-width="1"/>
  <line x1="75" y1="115" x2="60" y2="120" stroke="#666" stroke-width="1"/>
  <line x1="165" y1="115" x2="190" y2="120" stroke="#666" stroke-width="1"/>

  <line x1="460" y1="50" x2="460" y2="40" stroke="#666" stroke-width="1"/>
  <line x1="510" y1="70" x2="520" y2="65" stroke="#666" stroke-width="1"/>
  <line x1="500" y1="110" x2="525" y2="120" stroke="#666" stroke-width="1"/>

  <line x1="260" y1="315" x2="220" y2="330" stroke="#666" stroke-width="1"/>
  <line x1="300" y1="330" x2="320" y2="340" stroke="#666" stroke-width="1"/>
  <line x1="340" y1="315" x2="380" y2="330" stroke="#666" stroke-width="1"/>
</svg>

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
