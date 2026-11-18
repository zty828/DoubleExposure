# DoubleExposure — UE 5.9 · PICO 一体机 VR ·「双重曝光」参赛工程

> PICO 2026 开发者大赛「最佳沉浸内容创作」赛道参赛作品：**VR 时间编辑解谜 + 轻战斗**「双重曝光 / DOUBLE EXPOSURE」。
> 核心玩法 = 三动词时间语法（世界切换 / 单物体回溯 / 记录提取）+ 锚定规则「你动过的东西，跨时间线不变」。
> 引擎 UE 5.9 预览版（5.9.0-60351404+++UE5+Release-5.9）+ 自适配 PICOOpenXR 6.1.4 插件。
> 设计/生产文档见 `docs/GDD.md`、`docs/PRODUCTION.md`；大赛官方确认项调研见 `../docs/research/official-confirmations.md`。

## 1. 打开方式
- 双击 `DoubleExposure.uproject`（EngineAssociation=5.9），或 `UnrealEditor.exe DoubleExposure.uproject`。
- Win64 Editor 已编译（含插件全模块），可直接打开，无需重新 build。
- **启动地图：`/Game/Maps/L_FinalMap`**（白模搭建中，由项目所有者维护）。
- 历史地图 L_Blockout / L_Test 已于 2026-11-18 删除，不再存在；旧 README 中对它们的引用均已失效。
- 第三方商城资产包（`Content/Fab`、`Content/MWLandscapeAutoMaterial`）**不在本仓库内**，需自行从 Fab 获取后放入对应目录，详见 §12。缺失时编辑器会报引用缺失警告，不影响工程打开。

## 2. 已验证配置（2026-11-17 经 MCP 读 CDO/cvar 真值复验）
| 项 | 值 | 说明 |
|---|---|---|
| 移动着色路径 | Deferred（r.Mobile.ShadingPath=1） | Host59 验证组合；性能不达标回退 Forward(0) |
| 移动抗锯齿 | MSAA（r.Mobile.AntiAliasing=3）+ r.MSAACount=4 | PICO 官方推荐 4x；PICO 4 可 2x |
| MultiView | vr.MobileMultiView=true | 移动 VR 必开，draw call 减半 |
| GI / 反射 | None / None | 禁 Lumen/SSGI/SSR；用烘焙 + Reflection Capture |
| Nanite / 光追 / 路径追踪 | 全 false | r.Nanite.ProjectEnabled=False（注意不是 r.Nanite） |
| 网格距离场 / VSM / DF 阴影 | 全 false | 距离场在 RendererSettings；VSM/DF 阴影在 [ConsoleVariables] |
| 静态光照 | true | 烘焙 lightmap 路线 |
| 后处理 | MotionBlur/AutoExposure/AO/LensFlare 等全关 | VR 舒适 + 移动性能 |
| PICO | DisableRHIThread=true；FFR=Medium+Dynamic（插件 Foveation，非引擎内置）；ParallelCamera=true；眼/脸/体/手追踪全关；HandInteractionEXT=true；MR 全关 | 与 Host59 基线一致 |
| Android | MinSDK=29、arm64、Vulkan、无 ES31、bPackageForOpenXRImmersive=True、pvr.app.type=vr | OpenXR 沉浸式 VR 包 |

配置主体在 `Config/DefaultEngine.ini`（RendererSettings / [ConsoleVariables] / PICOOpenXRRuntimeSettings / AndroidRuntimeSettings / OpenXRHMD / Portal 各节，含中文注释）。

## 3. 目录结构
- `Config/` 工程配置（DefaultEngine/DefaultGame/DefaultInput 等）。
- `Content/Maps/L_FinalMap.umap` 当前默认启动/打包图（白模，项目所有者维护）。
- `Content/DoubleExposure/` 本作自有游戏内容。
- `Content/DoubleExposure/Materials/` 自制移动 VR 河水材质（2026-11-18）：`M_River_Mobile`（Translucent + Default Lit + TLM_Surface，双 Panner 法线 + SceneDepth 深度渐变 + 岸线泡沫 + Fresnel，全参数化）+ `MI_River` 实例 + `T_RiverNormal` 程序化无缝法线 512²（生成脚本 `Tools/water/gen_normal.py`）。刻意不用 SingleLayerWater——其在 VR 前向 + 实例化立体下不渲染（UE5.4+ 已知问题）。
- `Content/XRFramework/` VR 模板核心（角色/抓握/交互，见 §9）；`Content/LevelPrototyping|Weapons|XRMannequins|VRSpectator/` 模板依赖资源包（按 MountName 挂载，勿改名）。
- `Content/Fab/`、`Content/MWLandscapeAutoMaterial/` 第三方商城资产（**仓库排除**，见 §12）。
- `Source/DoubleExposure/` 最小空游戏模块（Runtime）。
- `Plugins/PICOOpenXR/` 自适配插件（源+内容+着色器；同源交付见 GitHub zty828/PICOOpenXR-UE5.9）。
- `Plugins/Tripo3DUEBridge/` Tripo3D 图生 3D 桥接插件（UE5.9 适配版，2026-11-18；编辑器 窗口→Tripo Bridge，ws://127.0.0.1:60620，配合 Tripo Studio 推模型入工程）。
- `docs/` GDD.md + PRODUCTION.md。
- `Binaries/ Intermediate/ Saved/ DerivedDataCache/ Plugins/**/Binaries|Intermediate/` 为**可再生构建产物**，已被 .gitignore 忽略；git clone 得到纯源码树，首次打开需编译。

## 4. 安卓打包与大赛口径
- 用 BuildCookRun 出正式 APK+OBB（裸 UBT APK 在旧模拟器镜像可能卡 PreInit）。
- 目标帧率 ≥72fps（PICO 商店历史底线），Ultra 90Hz 为目标。
- **大赛不要求过 PICO 商店审核**（官方细则 PDF 证实）；准入硬指标=可安装启动退出 + 核心流程可走通 + **连续运行 30 分钟无崩溃**。获奖后发布到 VibeLab 平台。
- 提交物=安装包 + GitHub 仓库 + Commit ID + 作品介绍 + 平台素材；**不强制开源**（开源为完成度加分项）。详见 ../docs/research/official-confirmations.md。

## 5. 编辑器 MCP（自动化验收通道）
- 编辑器启动自动 LISTEN `127.0.0.1:8000/mcp`；工具集全名带前缀（EditorToolset.LevelToolset / AssetToolset / ObjectToolset / EditorAppToolset）。
- Python：`editor_toolset.toolsets.python_scripting.PythonScriptingTools.execute_python`，参数 `{script:{content,language:"Python"}}`；**脚本末尾放表达式**才回传值（print 不回传）。
- 读设置真值：ObjectToolset.GetProperties{instance:{refPath:"/Script/Engine.Default__RendererSettings"},properties:[...]}；读 cvar：unreal.SystemLibrary.get_console_variable_*_value。

## 6. 已知无害日志噪声（非项目问题）
- 13× `LogAutomationTest: Error: Condition failed`（前置 UE::UnifiedErrorTest）= 引擎统一错误框架自测，每次启动固有。
- `Wintab32.dll` 缺失 = 数位板驱动，无影响。
- `Multiview rendering is not supported for PCD3D_SM5` = 桌面预览警告；移动端 Vulkan 正常。
- `LogPICOOpenXRHMD: Skipping xrEnumerateSystemExtensionPropertiesEXT` 高频刷屏 = PICO 扩展在非 PICO 运行时下的优雅跳过，无害。

## 7. 验证证据
- 截图：`../logs/DoubleExposure_editor_boot.png`、`../logs/DoubleExposure_editor_verify.png`（PICO Op_Portal 显示 SDK 6.1.4 / 支持 UE5.9+，Vulkan/Multiview/SDK29 三项 valid）。
- 日志：`../logs/DoubleExposure_editor_boot.log`、`../logs/DoubleExposure_editor_verify.log`。

## 8. PCVR 桌面预览（Pimax Dream Air，2026-11-17 增配并复验）
- 目的：真机 PICO 到手前用本机 Pimax Dream Air + Pimax OpenXR 运行时做 VR Preview 开发调试；**不改变 Android/PICO 目标配置**。
- 新增（仅桌面生效）：.uproject 加 OpenXREyeTracker+OpenXRHandTracking（保留 PICOOpenXR/PICOController）；DefaultEngine 加 r.ForwardShading=True、vr.InstancedStereo=True、[WindowsTargetPlatform] D3D12 SM6/D3D11 SM5；DefaultGame bStartInVR=True；DefaultInput 合并模板 82 条手柄/观战映射。
- 移动基线不变：MobileShadingPath=Deferred、MSAA4、MultiView、Android Vulkan/arm64/MinSDK29 等保持原值（MCP 复验确认）。
- **共存原理与实证**：PICOOpenXR 是 IOpenXRExtensionPlugin（扩展插件），不接管运行时；运行时由 OS 活跃 OpenXR 运行时（注册表 ActiveRuntime=Pimax PiOpenXR_64.json）决定。日志 logs/DoubleExposure_pcvr_verify.log：`Mounting Project plugin PICOOpenXR` + `LogPICOOpenXRHMD: PICO OpenXR PostCreateInstance RuntimeName:Pimax OpenXR` + PICO 扩展优雅跳过 + 枚举到 Pimax 的 eye_gaze/hand_tracking/VARJO_foveated。
- 测试：连 Dream Air→Pimax Play RUNTIME=Pimax OpenXR→打开本工程→VR Preview。截图 logs/DoubleExposure_pcvr_verify.png。
- 注意：重编前需关闭其它 UE 编辑器/LiveCoding（会锁引擎模块）。
- **已知渲染坑**：桌面 Forward+InstancedStereo 下 UE Water 插件的 SingleLayerWater 材质不渲染（UE5.4+ 前向+VR 已知问题）；移动 VR 水材质方案见 ../docs/research/water-material-ue59-mobile.md。

## 9. VR 模板核心（XRFramework，正式开发基座）
- 已从 UE 自带 VR 模板（XRFramework）整体移植角色/抓握/交互核心到本工程，挂载路径与模板一致（/Game/XRFramework/...），引用零缺失。
- **核心蓝图读法**（Content/XRFramework/Blueprints/）：
  - `BP_XRGameMode`：游戏模式，指定默认 Pawn=BP_XRPawn。已设为 GlobalDefaultGameMode。
  - `BP_XRPawn`：VR 角色。含相机/左右 MotionController、传送、snap turn、抓握调用。开发时主要改这里。
  - `BP_GrabComponent`：抓握组件（挂在 Pawn 手上），实现 trace→判定→抓取逻辑链。
  - `BP_Grabbable_SmallCube`：可抓物体示例（实现抓握接口），新道具可仿照它。
  - `BP_TeleportVisualizer`/`BP_Menu`/`WBP_Menu`：传送指示/菜单 UI。
  - `BP_Pistol`/`BP_Projectile`：枪械/弹丸示例（轻战斗可参考）。
  - `E_GrabType`/`BPI_PawnAnim`：抓握类型枚举/动画接口。
- **历史经验（原 L_Test 测试图，地图已删，结论仍有效）**：
  - 追踪原点=Stage（地板=0，HMD 提供真实身高）→ PlayerStart z=0、BP_XRPawn base_eye_height=0，眼高=真实身高。
  - 传送需 NavMeshBoundsVolume + exec `BuildNavigation`（RebuildNavigation/BuildPaths 无效）；换新地图需重加导航+重建。
  - 光照层次感：锁曝光（GlobalPP histogram min=max=1）+强主光弱补光+动态阴影；auto-exposure 会抹平对比。
  - 天空球 sun_height 高=白天、低=黄昏；DirectionalLightActor=None 才能固定 sun_height。
  - 白模几何用 `/Engine/BasicShapes/Cube.Cube`（中心原点）；`SM_Cube` bounds origin=(50,50,50) 会偏移半尺寸。

## 10. 白模交接（2026-11-18）
- 项目所有者删除此前助手搭建的全部地图（L_Test/L_Blockout），自建 `/Game/Maps/L_FinalMap` 并自行搭建白模。
- 方向：整体尺度放大、白天保留天空、室内为主+适当室外；第一关=吊桥户外→室内实验室（复杂化）。
- 助手侧约定：未经新指令不改动 UE 场景/地图/资产；玩法原型在独立测试图开发，不触碰 L_FinalMap。

## 11. 下一步
- W1（11/17–11/23）：三动词最小原型（独立测试图）+ 真机/模拟器基线。
- 报名/提交：11/25 提交通道开放；**报名与提交同于 12/19 09:00（UTC+8）截止**；12/26 北京大钟寺决赛路演（差旅自理）。报名材料终稿见 `../docs/contest/registration.md`。
- 游戏内容按 docs/PRODUCTION.md 里程碑推进。

## 12. 许可证与第三方资产
- **本仓库自有内容（Source/、Config/、docs/、Content/DoubleExposure/、Content/Maps/ 自有地图、插件适配改动）以 MIT 许可证开源**（见 LICENSE），对应大赛完成度维度「开源、可被其他开发者二次开发」加分。
- **仓库排除的第三方商城资产**（Fab EULA 禁止原样再分发；体积原因）：
  - `Content/Fab/`：Megascans 岩石/材质等（Fab 免费/已购资产，自行从 fab.com 获取导入）。
  - `Content/MWLandscapeAutoMaterial/`：地形自动材质包（含 54MB 示例图；L_FinalMap 地形引用其材质，缺失时地形显示默认材质，不影响运行）。
- `Content/XRFramework|LevelPrototyping|Weapons|XRMannequins|VRSpectator/` 来自 UE 自带 VR 模板，受 UE EULA 约束，仅随本工程用于参赛评审，不得单独提取再分发。
- `Plugins/PICOOpenXR/` 基于 PICO 官方 SDK 6.1.4 的 UE5.9 自适配版，同源公开仓库 https://github.com/zty828/PICOOpenXR-UE5.9 ；PICO SDK 部分权利归 PICO 所有。
- `Plugins/Tripo3DUEBridge/` 基于 Tripo3D 官方 UE 桥接插件的 UE5.9 适配（仅 uplugin 依赖声明改动），权利归 Tripo3D 所有。
