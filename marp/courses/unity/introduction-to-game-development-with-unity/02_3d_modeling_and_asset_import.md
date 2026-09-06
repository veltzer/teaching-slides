---
tags:
  - tools:unity
  - practices:3d
level: beginner
category: game-development
audience:
  - audiences:developers

---

# 3D Modeling and Asset Import

---

## Common Texture Maps

![texture_types](svg/courses/unity/introduction-to-game-development-with-unity/02_3d_modeling_and_asset_import/texture_types.svg)

---

## What This Chapter Covers

- The vocabulary of 3D modeling — meshes, vertices, polygons, UVs
- Materials and textures
- Bringing models in from external tools
- The Asset Store
- Keeping import settings sane for performance

---

## What a 3D Model Is, Roughly

- A bag of points (vertices) in 3D space
- Triples of vertices form triangles (the only thing GPUs really draw)
- A surface = a connected set of triangles
- A *normal* per vertex tells the shader which way is "out"
- *UV coordinates* tell the shader where to sample the texture

---

## Polygon Counts

- Triangles per object is a real cost — both memory and per-frame work
- Mobile target: ~10k triangles per character is generous
- Desktop / console target: 50k+ per character is fine
- VR: cut these in half — every frame is rendered twice
- Modern engines have LOD (level-of-detail) systems to swap in lower-poly versions at distance

---

## Materials and Shaders

- A *shader* is the program that decides each pixel's colour
- A *material* is a shader plus its inputs (textures, colours, numbers)
- One shader can drive many materials
- One material can be reused across many objects (a "GPU instance")
- Built-in shaders: Standard, Unlit, Universal Render Pipeline shaders

---

## Textures

- Image files (PNG, JPG, EXR, etc.) wrapped onto surfaces
- Common textures: albedo (base colour), normal, metallic, roughness, ambient occlusion
- Texture size is a memory and bandwidth cost — keep it sane
- Power-of-two sizes (256, 512, 1024, 2048) compress better
- Unity's import settings control compression per-platform

---

## Mesh Pipeline

![mesh_pipeline](svg/courses/unity/introduction-to-game-development-with-unity/02_3d_modeling_and_asset_import/mesh_pipeline.svg)

---

## Modeling Inside Unity

- Unity is *not* a modeling tool — it has primitives but no polygon-edit mode
- ProBuilder package: built-in level prototyping (extrude, bevel, subdivide)
- Use ProBuilder for blockouts and grey-box levels
- Move to Blender / Maya / 3ds Max for production-quality models
- ProBuilder meshes can be exported to FBX for further work

---

## External Modeling Tools

- **Blender**: free, open source, very capable
- **Maya**: industry standard for animation
- **3ds Max**: popular in architecture and games
- **ZBrush**: high-detail sculpting (then retopologise to a low-poly mesh)
- All export to FBX or OBJ, both of which Unity reads

---

## Importing a Model

- Drop the FBX / OBJ file into your project's `Assets` folder
- Unity processes it and creates a `.meta` file alongside
- Click the model in the Project window to see import settings in the Inspector
- Settings are split into Model, Rig, Animation, Materials tabs
- Hit Apply after changes — Unity re-imports

---

## Common Import Settings

- **Scale Factor**: usually 1.0; some tools export at cm vs m and need 100x or 0.01x
- **Mesh Compression**: low/medium/high — saves disk and memory at slight quality loss
- **Generate Lightmap UVs**: tick if you'll bake lighting onto this object
- **Normals**: Import (use what the artist exported) vs Calculate (Unity computes)
- **Materials**: Extract Materials creates editable material assets

---

## Texture Import Settings

- **Type**: Default for normal textures, Normal Map for bumpy surface data
- **Max Size**: cap the size per platform; 2048 is plenty for most things
- **Compression**: ASTC for mobile, BC for PC
- **Mip Maps**: keep on; Unity generates smaller versions for distant rendering
- Wrong settings can destroy quality or balloon memory — review every texture

---

## Materials in Unity

- Right-click in the Project window &#8594; Create &#8594; Material
- Pick a shader (Standard is the default)
- Assign textures to the slots (Albedo, Normal, Metallic, etc.)
- Drag the material onto a GameObject in the Scene to apply it
- One material can be shared across hundreds of GameObjects — keeps draw calls down

---

## The Asset Store

- Marketplace inside Unity Hub
- Free and paid 3D models, textures, scripts, full systems
- Filter by Unity version compatibility
- Read reviews — quality is wildly variable
- Always verify the licence terms; some assets restrict commercial use

---

## Optimising for Performance

- Combine many small static meshes into batches (Static Batching)
- Reuse materials and textures across many objects
- Reduce overdraw — overlapping transparent surfaces are expensive
- Bake static lighting where possible
- Profile with Unity's Frame Debugger before optimising

---

## A Quick Sanity Pipeline

- Always check the polygon count of imported models (Inspector preview)
- Always check the texture size and memory footprint
- Always assign materials before duplicating an object 100 times
- Keep your `Assets` folder organised: Models, Textures, Materials, Prefabs, Scripts
- Naming convention: `pf_PlayerCharacter`, `mat_GroundDirt`, `tex_GroundDirt_albedo`

---

## Common Beginner Mistakes

- Importing a model at 100x scale and then scaling it down inside the editor (use import scale)
- Letting Unity create a separate material for every imported FBX — leads to hundreds of duplicates
- Using uncompressed 8K textures for a phone game
- Forgetting to set the texture type to Normal Map for bump textures (looks horribly wrong)
- Modeling in the editor — possible but painful; use a real tool
