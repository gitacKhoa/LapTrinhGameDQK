// Assets/Editor/LivingFarmSpriteSlicer.cs  (bản thay thế cho bản ở 01_Environment)
// CHƯA kiểm thử trong Unity 6000.3.11f1. Chọn sheet PNG -> chuột phải -> Living Farm > Slice Sheet (names.txt)
// names.txt: dòng đầu tùy chọn "#cell=WxH pivot=center|bottom" (mặc định 16x16 center), các dòng sau là tên sprite
// theo thứ tự trái->phải, trên->dưới.
using System.Collections.Generic;
using System.IO;
using UnityEditor;
using UnityEditor.U2D.Sprites;
using UnityEngine;

public static class LivingFarmSpriteSlicer
{
    const int PPU = 16;

    [MenuItem("Assets/Living Farm/Slice Sheet (names.txt)")]
    static void Slice()
    {
        foreach (var obj in Selection.objects)
        {
            var path = AssetDatabase.GetAssetPath(obj);
            var namesPath = Path.ChangeExtension(path, ".names.txt");
            if (!File.Exists(namesPath)) { Debug.LogWarning($"Thiếu {namesPath}"); continue; }
            var lines = new List<string>(File.ReadAllLines(namesPath));
            int cw = 16, ch = 16; bool bottom = false; bool custom = false; Vector2 customPivot = new Vector2(0.5f, 0.5f);
            if (lines.Count > 0 && lines[0].StartsWith("#"))
            {
                foreach (var tok in lines[0].TrimStart('#').Split(' '))
                {
                    if (tok.StartsWith("cell=")) { var p = tok.Substring(5).Split('x'); cw = int.Parse(p[0]); ch = int.Parse(p[1]); }
                    if (tok == "pivot=bottom") bottom = true;
                    if (tok.StartsWith("pivot=") && tok.Contains(",")) { var q = tok.Substring(6).Split(','); customPivot = new Vector2(float.Parse(q[0], System.Globalization.CultureInfo.InvariantCulture), float.Parse(q[1], System.Globalization.CultureInfo.InvariantCulture)); custom = true; }
                }
                lines.RemoveAt(0);
            }

            var importer = (TextureImporter)AssetImporter.GetAtPath(path);
            importer.textureType = TextureImporterType.Sprite;
            importer.spriteImportMode = SpriteImportMode.Multiple;
            importer.spritePixelsPerUnit = PPU;
            importer.filterMode = FilterMode.Point;
            importer.textureCompression = TextureImporterCompression.Uncompressed;
            importer.mipmapEnabled = false;
            importer.alphaIsTransparency = true;
            importer.SaveAndReimport();

            var tex = AssetDatabase.LoadAssetAtPath<Texture2D>(path);
            int cols = tex.width / cw, rows = tex.height / ch;
            var factory = new SpriteDataProviderFactories(); factory.Init();
            var dp = factory.GetSpriteEditorDataProviderFromObject(importer);
            dp.InitSpriteEditorDataProvider();

            var rects = new List<SpriteRect>();
            for (int i = 0; i < lines.Count && i < cols * rows; i++)
            {
                if (string.IsNullOrWhiteSpace(lines[i])) continue;
                int cx = i % cols, cy = i / cols;
                rects.Add(new SpriteRect
                {
                    name = lines[i].Trim(),
                    spriteID = GUID.Generate(),
                    rect = new Rect(cx * cw, tex.height - (cy + 1) * ch, cw, ch),
                    alignment = custom ? SpriteAlignment.Custom : (bottom ? SpriteAlignment.BottomCenter : SpriteAlignment.Center),
                    pivot = custom ? customPivot : (bottom ? new Vector2(0.5f, 0f) : new Vector2(0.5f, 0.5f))
                });
            }
            dp.SetSpriteRects(rects.ToArray());
            var idp = dp.GetDataProvider<ISpriteNameFileIdDataProvider>();
            var pairs = new List<SpriteNameFileIdPair>();
            foreach (var r in rects) pairs.Add(new SpriteNameFileIdPair(r.name, r.spriteID));
            idp.SetNameFileIdPairs(pairs);
            dp.Apply();
            importer.SaveAndReimport();
            Debug.Log($"Đã cắt {rects.Count} sprite ({cw}x{ch}): {path}");
        }
    }
}
