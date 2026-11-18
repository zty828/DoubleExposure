import unreal,json
L=unreal.MaterialEditingLibrary
m=unreal.load_asset('/Game/DoubleExposure/Materials/M_River_Mobile.M_River_Mobile')
m.modify()
ex={e.get_name():e for e in L.get_material_expressions(m)}
def prop(n,p,v):
 ex[n].set_editor_property(p,v)
def scalar(name,val):
 prop(name,'default_value',float(val))
# Two low-contrast organic layers, no high-frequency procedural detail.
scalar('MaterialExpressionScalarParameter_28',0.85)
scalar('MaterialExpressionScalarParameter_29',0.43)
scalar('MaterialExpressionScalarParameter_30',1.0)
scalar('MaterialExpressionScalarParameter_31',0.07)
scalar('MaterialExpressionScalarParameter_33',0.7)
scalar('MaterialExpressionScalarParameter_34',0.25)
scalar('MaterialExpressionScalarParameter_35',0.20)
scalar('MaterialExpressionScalarParameter_36',0.0)
scalar('MaterialExpressionScalarParameter_42',0.055)
scalar('MaterialExpressionScalarParameter_43',0.35)
# Disable the fine-detail branch completely before removing it.
L.disconnect_material_expressions(ex['MaterialExpressionAdd_5'],'B')
L.connect_material_expressions(ex['MaterialExpressionAdd_4'],'',ex['MaterialExpressionNormalize_2'],'VectorInput')
# Preserve depth color and shore fade; tame the artificial cyan Fresnel tint.
prop('MaterialExpressionVectorParameter_12','default_value',unreal.LinearColor(0.035,0.18,0.205,1))
prop('MaterialExpressionVectorParameter_13','default_value',unreal.LinearColor(0.008,0.055,0.080,1))
prop('MaterialExpressionVectorParameter_15','default_value',unreal.LinearColor(0.42,0.54,0.64,1))
prop('MaterialExpressionConstant_17','r',0.10)
prop('MaterialExpressionFresnel_2','exponent',5.0)
prop('MaterialExpressionFresnel_2','base_reflect_fraction',0.02)
prop('MaterialExpressionConstant_18','r',1.0)
prop('MaterialExpressionTextureSampleParameter2D_6','parameter_name','NormalBroad')
prop('MaterialExpressionTextureSampleParameter2D_7','parameter_name','NormalRipples')
prop('MaterialExpressionTextureSampleParameter2D_6','desc','Water organic normal: broad, low-amplitude layer')
prop('MaterialExpressionTextureSampleParameter2D_7','desc','Water organic normal: sparse cross-flow, non-integer scale')
for name in ['MaterialExpressionMultiply_27','MaterialExpressionPanner_8','MaterialExpressionMultiply_25','MaterialExpressionMultiply_26','MaterialExpressionConstant_16','MaterialExpressionTextureCoordinate_8','MaterialExpressionTextureSampleParameter2D_8']:
 if name in ex:L.delete_material_expression(m,ex[name])
L.delete_unused_expressions(m)
warnings=L.recompile_material(m)
L.layout_material_expressions(m)
unreal.EditorAssetLibrary.save_loaded_asset(m,only_if_is_dirty=False)
mi=unreal.load_asset('/Game/DoubleExposure/Materials/MI_River.MI_River')
unreal.EditorAssetLibrary.save_loaded_asset(mi,only_if_is_dirty=True)
json.dumps({'saved':m.get_path_name(),'warnings':[str(x) for x in warnings],'nodes':L.get_num_material_expressions(m),'parameters':{str(e.get_editor_property('parameter_name')):e.get_editor_property('default_value') for e in L.get_material_expressions(m) if isinstance(e,unreal.MaterialExpressionScalarParameter)},'stats':str(L.get_statistics(m))})