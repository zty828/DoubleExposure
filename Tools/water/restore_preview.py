import unreal,json
unreal.EditorSubsystemBlueprintLibrary.disable_preview_platform()
json.dumps({'platform':str(unreal.EditorSubsystemBlueprintLibrary.get_preview_platform_name())})