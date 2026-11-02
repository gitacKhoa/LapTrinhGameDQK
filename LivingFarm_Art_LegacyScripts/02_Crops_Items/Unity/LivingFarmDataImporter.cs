// Assets/Editor/LivingFarmDataImporter.cs - CHƯA kiểm thử trong Unity.
// Menu: Tools > Living Farm > Create Data Assets From CSV
// Cần: Assets/Data/Source/items.csv, crops.csv; sprite đã được cắt: Assets/Art/Items/items_16.png, Assets/Art/Crops/crops_sheet.png
using System.Collections.Generic;
using System.IO;
using System.Linq;
using UnityEditor;
using UnityEngine;

public static class LivingFarmDataImporter
{
    const string ItemsCsv = "Assets/Data/Source/items.csv";
    const string CropsCsv = "Assets/Data/Source/crops.csv";
    const string ItemSheet = "Assets/Art/Items/items_16.png";
    const string CropSheet = "Assets/Art/Crops/crops_sheet.png";
    const string ItemOut = "Assets/Data/Items";
    const string CropOut = "Assets/Data/Crops";

    static Dictionary<string, Sprite> Sprites(string sheet) =>
        AssetDatabase.LoadAllAssetsAtPath(sheet).OfType<Sprite>().ToDictionary(s => s.name, s => s);

    static void Ensure(string dir)
    {
        if (!AssetDatabase.IsValidFolder(dir))
        {
            var parent = Path.GetDirectoryName(dir).Replace('\\', '/');
            AssetDatabase.CreateFolder(parent, Path.GetFileName(dir));
        }
    }

    [MenuItem("Tools/Living Farm/Create Data Assets From CSV")]
    static void Run()
    {
        Ensure("Assets/Data"); Ensure(ItemOut); Ensure(CropOut);
        var itemSprites = Sprites(ItemSheet); var cropSprites = Sprites(CropSheet);
        var items = new Dictionary<string, ItemData>();

        foreach (var row in Rows(ItemsCsv))
        {
            var p = $"{ItemOut}/Item_{row["id"]}.asset";
            var it = AssetDatabase.LoadAssetAtPath<ItemData>(p);
            if (it == null) { it = ScriptableObject.CreateInstance<ItemData>(); AssetDatabase.CreateAsset(it, p); }
            it.id = row["id"]; it.displayName = row["displayName"]; it.description = row["description"];
            it.category = System.Enum.Parse<ItemCategory>(row["category"]);
            it.maxStack = int.Parse(row["maxStack"]); it.buyPrice = int.Parse(row["buyPrice"]); it.sellPrice = int.Parse(row["sellPrice"]);
            itemSprites.TryGetValue(row["sprite"], out it.icon);
            if (it.icon == null) Debug.LogWarning($"Không thấy sprite {row["sprite"]}");
            EditorUtility.SetDirty(it); items[it.id] = it;
        }

        foreach (var row in Rows(CropsCsv))
        {
            var p = $"{CropOut}/Crop_{row["id"]}.asset";
            var c = AssetDatabase.LoadAssetAtPath<CropData>(p);
            if (c == null) { c = ScriptableObject.CreateInstance<CropData>(); AssetDatabase.CreateAsset(c, p); }
            c.id = row["id"]; c.displayName = row["displayName"];
            items.TryGetValue(row["seedItem"], out c.seedItem); items.TryGetValue(row["harvestItem"], out c.harvestItem);
            c.daysPerStage = row["daysPerStage"].Split(';').Select(int.Parse).ToArray();
            c.growSeasons = row["seasons"].Split(';').Select(s => System.Enum.Parse<Season>(s)).Aggregate(Season.None, (a, b) => a | b);
            c.regrows = row["regrows"] == "1"; c.regrowDays = int.Parse(row["regrowDays"]);
            c.harvestYield = new Vector2Int(int.Parse(row["yieldMin"]), int.Parse(row["yieldMax"]));
            string[] st = { "seed", "sprout", "growing", "mature", "ready" };
            c.stageSprites = st.Select(s => cropSprites.TryGetValue($"crop_{c.id}_{s}", out var sp) ? sp : null).ToArray();
            cropSprites.TryGetValue($"crop_{c.id}_wilted", out c.wiltedSprite);
            EditorUtility.SetDirty(c);
        }
        AssetDatabase.SaveAssets(); AssetDatabase.Refresh();
        Debug.Log("Living Farm: đã tạo/cập nhật dữ liệu từ CSV.");
    }

    static IEnumerable<Dictionary<string, string>> Rows(string path)
    {
        var lines = File.ReadAllLines(path).Where(l => !string.IsNullOrWhiteSpace(l)).ToArray();
        var head = lines[0].Split(',');
        for (int i = 1; i < lines.Length; i++)
        {
            var v = lines[i].Split(',');
            yield return head.Select((h, k) => (h, k)).ToDictionary(t => t.h.Trim(), t => v[t.k].Trim());
        }
    }
}
