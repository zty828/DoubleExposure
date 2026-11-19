# M_River_Mobile — v5 细波纹与天青色

## 本轮目标
保留 v4 消除密集高对比条纹的成果，补回可辨识的小波纹/流动细节，并将过深、偏蓝的水体提亮为天青色。

## 相对 v4 的调整
| 参数 | v4 | v5 |
|---|---:|---:|
| TilingA / TilingB | 0.85 / 0.43 | 0.85 / **1.65** |
| WeightA / WeightB | 0.8 / 0.18 | 0.8 / **0.42** |
| NormalStrength | 0.7 | **0.72** |
| ShallowColor (linear RGB) | 0.035, 0.18, 0.205 | **0.10, 0.38, 0.44** |
| DeepColor (linear RGB) | 0.008, 0.055, 0.08 | **0.035, 0.19, 0.26** |

- FlowSpeed 保持 0.07；本轮没有加快流速。
- 仍只有两层同一 1024² 有机法线采样，不恢复 v3 高频第三层。TilingB=1.65、WeightB=0.42，避免 v3 的 TilingC=7、WeightC=1.0 造成密集条纹。
- 提亮通过水体颜色完成，未新增 Emissive，未重新打开 Fresnel 天蓝染色。
- Roughness 0.055 / Specular 0.225；Translucent / DefaultLit；深度色、透明和岸边淡出保持不变。
- 本轮只保存 M_River_Mobile；MI_River 继续继承父材质，无标量、向量或纹理参数覆盖。

## 验证
- UE MCP 实际修改、保存并重编译 M_River_Mobile：0 warnings、0 expression errors。
- 默认桌面预览下，同一峡谷机位捕获 v5_before.png 和 v5_after.png。
- pixel instructions 839、pixel texture samples 3、samplers 7，与 v4 相同；这些是 UE 材质统计，不等于 GPU 耗时或真机帧率。
- 本轮不切换 Android 预览平台，避免重复触发上次恢复预览时的 D3D12 崩溃；仍需 PICO 真机核验动态观感与 72fps。

## 复现与范围
apply_v5.py 通过参数名定位节点，适用于 v4/v5 图结构。修改前核对 M_River_Mobile 资产；执行需使用 logs/water-assets/ue_mcp.js 的 UE MCP Python 通道。
没有保存或修改用户地图、地形、水体 Actor、菜单、XR Pawn 或工程设置。
