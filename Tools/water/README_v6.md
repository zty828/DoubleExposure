# 移动 VR 河流水材质 v6：固定世界尺度 + 天青色

## 根因与修复

v5 的两层法线使用 TextureCoordinate 0，平面对象 Scale 会把 UV 波纹同步拉伸。v6 删除对象 UV，按 UE Water 插件 `/Water/Materials/Functions/WaterTextureSurface` 的核心映射方式改为：

```
WorldPosition → ComponentMask(RG) → Divide(WaterScale) → ×TilingA/B → Panner → 同一有机法线的两次采样
```

平面对象缩放不再影响波纹密度。两条 Panner 节点链均回溯验证包含同一个 WorldPosition 和 WaterScale；材质内 TextureCoordinate 数量为 0。无需改动对象 UV、Scale 或地图。

## 已保存的最终参数

只修改并保存 `/Game/DoubleExposure/Materials/M_River_Mobile.M_River_Mobile`；`MI_River` 继承父材质，无 WaterScale/Tiling 覆盖。用户平面、地图、菜单与 XR Pawn 均未修改或保存。

| 参数 | 值 |
|---|---:|
| WaterScale | 1536 cm |
| TilingA / TilingB | 0.85 / 1.65 |
| WeightA / WeightB | 0.70 / 0.35 |
| NormalStrength | 0.30 |
| FlowSpeed / FlowAngle | 0.07 / 0° |
| Roughness / Specular | 0.10 / 0.10 |
| ShallowColor（线性 RGB） | 0.18, 0.55, 0.58 |
| DeepColor（线性 RGB） | 0.10, 0.38, 0.40 |
| Opacity | 0.88 × 岸边深度淡出 |

主纹理重复尺度约 18.07 m，次级约 9.31 m；一个纹理内包含多组波纹，并非单个波纹长度。统一调整密度时只调 **WaterScale**：越大波纹越疏，越小越密；TilingA/B 只调整两层之间的相对尺度。

## 验证

- `finalize_v6.py`：两条 Panner 链均回溯到 WorldPosition/WaterScale，无 TextureCoordinate。
- 两层仍使用同一张 1024² `T_RiverDetail_Normal`，没有新增法线纹理或 Emissive/Fresnel 染色。
- UE 材质重编译：0 warnings、0 errors；桌面 SM6 统计为 844 pixel instructions、6 pixel texture samples、7 samplers（不是 GPU 毫秒或移动真机结论）。
- 编辑器预览平台 None，未切换预览以避免此前描述符缓存崩溃。移动端实际帧率需后续 PICO 真机测量。
- 同机位验证图：`logs/water-assets/v6_before.png`、`v6_final.png`。不声称与 Water 插件逐像素一致。

## 复现

1. 在 v5 父材质上执行 `apply_v6.py`，只执行一次：创建 WorldPosition/RG/WaterScale 并删除对象 UV。
2. 执行 `finalize_v6.py`：应用最终外观参数，验证世界坐标链、继承与编译结果，保存唯一目标材质。
3. 执行方式：UE 编辑器 MCP 的 `execute_python`，参数 `script={content:<文件源码>,language:'Python'}`；末尾表达式返回 JSON。
