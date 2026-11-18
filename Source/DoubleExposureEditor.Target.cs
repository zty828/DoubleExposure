using UnrealBuildTool;
using System.Collections.Generic;

public class DoubleExposureEditorTarget : TargetRules
{
	public DoubleExposureEditorTarget(TargetInfo Target) : base(Target)
	{
		Type = TargetType.Editor;
		DefaultBuildSettings = BuildSettingsVersion.Latest;
		IncludeOrderVersion = EngineIncludeOrderVersion.Latest;
		ExtraModuleNames.Add("DoubleExposure");
	}
}
