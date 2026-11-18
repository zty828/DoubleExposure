# Tripo3D UE Bridge — UE5.9 预览版适配说明

## 结论
原压缩包内 UE5.8 预编译版（Tripo3DUEBridge-UE5.8-Win64）**不能**直接用于 UE5.9 预览版：
插件二进制与引擎 ABI 强绑定（.modules 的 BuildId + uplugin 的 EngineVersion="5.8.0"），
5.9（BuildId 60351404，CompatibleChangelist=0）会拒绝加载 5.8 的 DLL。

本目录是用压缩包内**纯源码变体 Tripo3d_UE_Bridge** 重新适配并编译的 UE5.9 版本，已验证可用。

## 适配改动（相对上游源码）
1. 选用无 EngineVersion 锁的纯源码变体（含完整 C++ 源码 + TripoVersionCompat.h 版本兼容层）。
2. Tripo3DUEBridge.uplugin 增加 Plugins 依赖声明：
   { "Name": "Interchange", "Enabled": true }
   （模块依赖 InterchangeEngine/InterchangePipelines，原 uplugin 漏声明，UBT 会告警）。
3. C++ 源码**零改动**：兼容层 UE_VERSION_AT_LEAST(5,8) 分支已覆盖 5.9，
   Interchange 动画 FrameAlignment=EInterchangeFrameAlignment::SnapToClosest 在 5.9 头文件中存在且匹配。
4. IXWebSocket.lib（预编译静态库）与 UE5.9 自带 zlib 1.3 链接通过，无 LNK 错误。

## 验证记录（2026-11-18）
- 宿主工程 PICOClean59（UE5.9，BuildSettingsVersion.V8 / Unreal5_9）：编译 Succeeded；
  编辑器运行时日志确认模块加载：
  LogModuleManager: InternalLoadLibrary 'Tripo3DUEBridge'
  LogTemp: Tripo Bridge module started successfully
- 主工程 DoubleExposure（UE5.9 + PICOOpenXR）：编译 Succeeded（121s），DLL 链接成功，与 PICOOpenXR 共存无冲突。
- 产物 UnrealEditor.modules BuildId=60351404，与引擎一致。

## 使用方法
1. 本插件已放入 DoubleExposure/Plugins/Tripo3DUEBridge 并在 .uproject 启用。
2. 打开 DoubleExposure.uproject（若提示重建模块选 Yes；已预编译则直接加载）。
3. 编辑器菜单 窗口(Window) → Tripo Bridge 打开桥接窗口，窗口打开即自动启动 WebSocket 服务（ws://127.0.0.1:60620）。
4. 在 Tripo Studio 侧连接该端口并推送模型（FBX/ZIP），插件自动导入到 /Game/TripoModels 并生成 PBR 材质与贴图。

## 重新编译（如需）
"D:\GameEngine\UE_5.9\Engine\Build\BatchFiles\Build.bat" DoubleExposureEditor Win64 Development -Project="F:\CG\Projects\PICOUE\DoubleExposure\DoubleExposure.uproject" -WaitMutex
注意：编译前须关闭所有 UE 编辑器（Live Coding 持引擎级全局锁，会拦截 UBT）。

## 工具链
VS2022 (F:\GameEngine\UE5.8.3Source\Tools\VS2022, MSVC 14.44) + Windows SDK 10.0.22621 + UE5.9 自带 zlib 1.3。
