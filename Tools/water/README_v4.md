# M_River_Mobile — v4

## 目标
移动端 VR 的轻量透明流水；参考 UE Water 插件有机法线与法线强度，不复制 SingleLayerWater、GBuffer、水体运行时。

## v4 相对 v3 的改动
- 删除 T_RiverFine_Normal 高频层及其 Panner/Tiling/Weight 分支。资产文件保留但不再采样。
- 两层同一 1024² 有机法线（T_RiverDetail_Normal），非整数倍错向流动。A 为主层，B 为弱错流。
- 移除水面 Fresnel 亮青色染色（乘法常数 0）。保留物理 Fresnel 高光、深度色、透明与岸边淡出。
- Specular 采用 Water 参考值 0.225；Roughness 0.055 避免大片高光过锐。
- 未改变 FlowSpeed 0.07、DepthFadeDistance 150、ShoreFadeDistance 60、FoamWidth 25、FoamIntensity 0.7。

## 默认参数
| 参数 | 值 |
|---|---:|
| TilingA / TilingB | 0.85 / 0.43 |
| WeightA / WeightB | 0.8 / 0.18 |
| NormalStrength | 0.7 |
| FlowSpeed / FlowAngle | 0.07 / 0 |
| ShallowColor | (0.035, 0.18, 0.205, 1) |
| DeepColor | (0.008, 0.055, 0.08, 1) |
| Roughness / Specular | 0.055 / 0.225 |
| Opacity | 0.88 × 岸边深度淡出 |

材质：Translucent / DefaultLit。第三层不采样、不留死节点；材质只使用一张 1024² 法线纹理。
纹理参数名为 NormalBroad 与 NormalRipples；材质实例无标量覆盖，继承以上默认值。

## 实测与边界
- UE 5.9、/Game/Maps/L_FinalMap 当前同机位视口截图。
- 已用 VULKAN_ES3_1_ANDROID Android_OpenXR 预览，M_River_Mobile 重编译 0 warnings、0 expression errors。
- 最终编辑器统计：pixel instructions 839，pixel texture samples 3，samplers 7。v3 为 866 / 4 / 7。统计包含引擎材质模板，不能换算成 GPU 毫秒或宣称真机帧率达标。
- 预览恢复为 None 后发生 D3D12 崩溃；日志为 `Missing uniform buffer at slot 4, stage SF_Pixel`（D3D12DescriptorCache.cpp:732）。这是本次编辑器预览会话的崩溃事实，不据此归因为材质代码。
- 重启后已从磁盘重载材质和实例，父材质、参数、纹理均一致，重新编译 0 expression errors；预览为 None。
- 没有保存地图、地形、水体 Actor、菜单或工程设置；保留这些文件原有的未提交修改。
- 仍需在目标 PICO 设备上检查 72fps、双眼注视方向和动态波纹，并以用户场景观感决定下一轮微调。
- `post_crash.py` 可通过 `ue_mcp.js python` 重载并核验资产。崩溃日志在 Saved/Crashes/UECC-Windows-798D5D1B4EAE309BCE21A8B50967DA53_0001/DoubleExposure.log。

## 可复现脚本
先审阅当前资产再运行；apply_v4.py 针对 v3 的节点名，若资产结构改变不可直接重跑。v4_tune.py 调最终强度/高光，finish_graph.py 整理参数分组并恢复桌面预览。
日志截图与临时 API 审计脚本在 F:\CG\Projects\PICOUE\logs\water-assets。
