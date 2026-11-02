using UnityEngine;

public enum ItemCategory { Seed, Crop, Tool, Resource, AnimalProduct, Material, Fertilizer, Processed }

[CreateAssetMenu(menuName = "Living Farm/Item Data", fileName = "Item_")]
public class ItemData : ScriptableObject
{
    [Header("Định danh")]
    public string id;                  // trùng cột id trong items.csv, ví dụ "carrot"
    public string displayName;
    [TextArea] public string description;
    public ItemCategory category;

    [Header("Hiển thị")]
    public Sprite icon;                // 16x16, từ items_16.png

    [Header("Kinh tế / túi đồ")]
    [Min(1)] public int maxStack = 99;
    [Min(0)] public int buyPrice;      // 0 = không bán ở cửa hàng
    [Min(0)] public int sellPrice;

    [Header("Tiêu thụ (tùy chọn)")]
    public bool edible;
    public int energyRestore;
}
