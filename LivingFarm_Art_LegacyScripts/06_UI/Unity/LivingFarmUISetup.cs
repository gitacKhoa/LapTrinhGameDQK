// Assets/Editor/LivingFarmUISetup.cs - CHƯA kiểm thử trong Unity 6000.3.11f1.
// Menu: Tools > Living Farm > Setup UI Sprites. Đọc Assets/Art/UI/ui_sprites.csv và đặt Sprite (Single), PPU 16, Point,
// Uncompressed và 9-slice border cho từng PNG trong Assets/Art/UI/Sprites (và Icons).
using System.IO;
using UnityEditor;
using UnityEngine;

public static class LivingFarmUISetup
{
    const string Root = "Assets/Art/UI";

    [MenuItem("Tools/Living Farm/Setup UI Sprites")]
    static void Run()
    {
        var csv = $"{Root}/ui_sprites.csv";
        if (!File.Exists(csv)) { Debug.LogError($"Thiếu {csv}"); return; }
        var lines = File.ReadAllLines(csv); int n = 0;
        for (int i = 1; i < lines.Length; i++)
        {
            var v = lines[i].Split(','); if (v.Length < 7) continue;
            var path = FindPng(v[0]); if (path == null) { Debug.LogWarning($"Không thấy {v[0]}.png"); continue; }
            Setup(path, new Vector4(int.Parse(v[3]), int.Parse(v[4]), int.Parse(v[5]), int.Parse(v[6]))); n++;
        }
        foreach (var f in Directory.GetFiles($"{Root}/Icons", "icon_*.png", SearchOption.AllDirectories)) Setup(f.Replace('\\', '/'), Vector4.zero);
        AssetDatabase.SaveAssets(); AssetDatabase.Refresh();
        Debug.Log($"Đã thiết lập {n} sprite UI (có border 9-slice).");
    }

    static string FindPng(string name)
    {
        foreach (var f in Directory.GetFiles(Root, name + ".png", SearchOption.AllDirectories)) return f.Replace('\\', '/');
        return null;
    }

    static void Setup(string path, Vector4 border)   // border: left, bottom, right, top
    {
        var imp = (TextureImporter)AssetImporter.GetAtPath(path);
        imp.textureType = TextureImporterType.Sprite; imp.spriteImportMode = SpriteImportMode.Single;
        imp.spritePixelsPerUnit = 16; imp.filterMode = FilterMode.Point;
        imp.textureCompression = TextureImporterCompression.Uncompressed; imp.mipmapEnabled = false;
        imp.spriteBorder = border; imp.alphaIsTransparency = true;
        imp.SaveAndReimport();
    }
}
