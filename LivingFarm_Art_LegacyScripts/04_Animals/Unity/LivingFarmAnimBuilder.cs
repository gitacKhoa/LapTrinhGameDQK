// Assets/Editor/LivingFarmAnimBuilder.cs - CHƯA kiểm thử trong Unity 6000.3.11f1.
// Dùng sau khi đã cắt sheet bằng Slicer. Chọn sheet PNG (player/npc/animal) -> chuột phải ->
// Living Farm > Build Animator From Sheet. Tool tạo AnimationClip cho mỗi (anim, hướng) và 1 AnimatorController
// với tham số int "Anim" và "Dir" (Any State -> state tương ứng).
// Tên sprite: <prefix>_<anim>_<dir>_<NN>   (vd. player_a_walk_down_00, animal_cow_eat_left_02)
using System.Collections.Generic;
using System.IO;
using System.Linq;
using UnityEditor;
using UnityEditor.Animations;
using UnityEngine;

public static class LivingFarmAnimBuilder
{
    // thứ tự = giá trị tham số "Anim"
    public static readonly string[] AnimNames = { "idle", "walk", "hoe", "water", "harvest", "chop", "mine", "carry_idle", "carry_walk", "eat" };
    public static readonly string[] DirNames = { "down", "up", "left", "right" };
    static readonly Dictionary<string, (float fps, bool loop)> Cfg = new()
    {
        {"idle",(4,true)},{"walk",(8,true)},{"hoe",(10,false)},{"water",(8,false)},{"harvest",(8,false)},
        {"chop",(10,false)},{"mine",(10,false)},{"carry_idle",(4,true)},{"carry_walk",(8,true)},{"eat",(6,true)}
    };

    [MenuItem("Assets/Living Farm/Build Animator From Sheet")]
    static void Build()
    {
        foreach (var obj in Selection.objects)
        {
            var path = AssetDatabase.GetAssetPath(obj);
            var sprites = AssetDatabase.LoadAllAssetsAtPath(path).OfType<Sprite>().ToList();
            if (sprites.Count == 0) { Debug.LogWarning($"Chưa cắt sprite: {path}"); continue; }

            // gom theo (prefix, anim, dir)
            var groups = new Dictionary<(string prefix, string anim, string dir), SortedDictionary<int, Sprite>>();
            foreach (var s in sprites)
            {
                if (s.name.Contains("_expr_")) continue;
                var t = s.name.Split('_');
                if (t.Length < 4 || !int.TryParse(t[^1], out int frame)) continue;
                string dir = t[^2]; string rest = string.Join("_", t.Take(t.Length - 2));
                string anim = AnimNames.OrderByDescending(a => a.Length).FirstOrDefault(a => rest == a || rest.EndsWith("_" + a));
                if (anim == null || !DirNames.Contains(dir)) continue;
                string prefix = rest == anim ? "" : rest.Substring(0, rest.Length - anim.Length - 1);
                var key = (prefix, anim, dir);
                if (!groups.ContainsKey(key)) groups[key] = new SortedDictionary<int, Sprite>();
                groups[key][frame] = s;
            }

            var dirPath = Path.Combine(Path.GetDirectoryName(path), "Anim_" + Path.GetFileNameWithoutExtension(path)).Replace('\\', '/');
            if (!AssetDatabase.IsValidFolder(dirPath)) AssetDatabase.CreateFolder(Path.GetDirectoryName(path).Replace('\\', '/'), Path.GetFileName(dirPath));
            var ctrl = AnimatorController.CreateAnimatorControllerAtPath($"{dirPath}/{Path.GetFileNameWithoutExtension(path)}.controller");
            ctrl.AddParameter("Anim", AnimatorControllerParameterType.Int);
            ctrl.AddParameter("Dir", AnimatorControllerParameterType.Int);
            var sm = ctrl.layers[0].stateMachine;

            AnimatorState defaultState = null;
            foreach (var kv in groups.OrderBy(k => System.Array.IndexOf(AnimNames, k.Key.anim)).ThenBy(k => System.Array.IndexOf(DirNames, k.Key.dir)))
            {
                var (fps, loop) = Cfg[kv.Key.anim];
                var clip = new AnimationClip { frameRate = fps, name = $"{kv.Key.anim}_{kv.Key.dir}" };
                var frames = kv.Value.Values.ToList();
                var keys = new List<ObjectReferenceKeyframe>();
                for (int i = 0; i < frames.Count; i++) keys.Add(new ObjectReferenceKeyframe { time = i / fps, value = frames[i] });
                keys.Add(new ObjectReferenceKeyframe { time = frames.Count / fps, value = frames[^1] });
                AnimationUtility.SetObjectReferenceCurve(clip, EditorCurveBinding.PPtrCurve("", typeof(SpriteRenderer), "m_Sprite"), keys.ToArray());
                var settings = AnimationUtility.GetAnimationClipSettings(clip); settings.loopTime = loop; AnimationUtility.SetAnimationClipSettings(clip, settings);
                AssetDatabase.CreateAsset(clip, $"{dirPath}/{clip.name}.anim");

                var state = sm.AddState(clip.name); state.motion = clip;
                var tr = sm.AddAnyStateTransition(state);
                tr.hasExitTime = false; tr.duration = 0; tr.canTransitionToSelf = false;
                tr.AddCondition(AnimatorConditionMode.Equals, System.Array.IndexOf(AnimNames, kv.Key.anim), "Anim");
                tr.AddCondition(AnimatorConditionMode.Equals, System.Array.IndexOf(DirNames, kv.Key.dir), "Dir");
                if (clip.name == "idle_down") defaultState = state;
            }
            if (defaultState != null) sm.defaultState = defaultState;
            AssetDatabase.SaveAssets();
            Debug.Log($"Đã tạo {groups.Count} clip + controller trong {dirPath}");
        }
    }
}
