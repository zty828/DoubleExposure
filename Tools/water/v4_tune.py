import unreal,json
L=unreal.MaterialEditingLibrary;m=unreal.load_asset('/Game/DoubleExposure/Materials/M_River_Mobile.M_River_Mobile');m.modify()
ex={e.get_name():e for e in L.get_material_expressions(m)}
for n,v in {'MaterialExpressionScalarParameter_34':0.8,'MaterialExpressionScalarParameter_35':0.18,'MaterialExpressionScalarParameter_36':0.12,'MaterialExpressionScalarParameter_43':0.225}.items():
 if n in ex:ex[n].set_editor_property('default_value',v)
ex['MaterialExpressionConstant_17'].set_editor_property('r',0.0)
for n in ['MaterialExpressionScalarParameter_34','MaterialExpressionScalarParameter_35','MaterialExpressionScalarParameter_36']:
 if n in ex:
  ex[n].set_editor_property('slider_min',0.0);ex[n].set_editor_property('slider_max',1.0)
warnings=L.recompile_material(m);unreal.EditorAssetLibrary.save_loaded_asset(m,only_if_is_dirty=False)
json.dumps({'warnings':[str(x) for x in warnings],'stats':str(L.get_statistics(m)),'opacity':ex['MaterialExpressionConstant_18'].get_editor_property('r')})