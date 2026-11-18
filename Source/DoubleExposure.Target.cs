using UnrealBuildTool;
using System.Collections.Generic;

public class DoubleExposureTarget : TargetRules
{
	public DoubleExposureTarget(TargetInfo Target) : base(Target)
	{
		Type = TargetType.Game;
		DefaultBuildSettings = BuildSettingsVersion.Latest;
		IncludeOrderVersion = EngineIncludeOrderVersion.Latest;
		ExtraModuleNames.Add("DoubleExposure");
	}
}
