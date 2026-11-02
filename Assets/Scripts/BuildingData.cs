using System;
using UnityEngine;

[Serializable] public struct ItemCost { public ItemData item; public int amount; }

[CreateAssetMenu(menuName = "Living Farm/Building Data", fileName = "Building_")]
public class BuildingData : ScriptableObject
{
    [Header("Định danh")]
    public string id; public string displayName;
    [Header("Hiển thị")]
    public Sprite sprite;                      // sprite chính (bld_*.png, machine_*_idle)
    [Header("Vùng chiếm chỗ (đơn vị tile, 1 tile = 16 px)")]
    public Vector2Int footprintTiles = Vector2Int.one;
    [Tooltip("Offset collider so với pivot (Bottom Center), đơn vị Unity unit (px/16).")]
    public Vector2 colliderOffset; public Vector2 colliderSize = new Vector2(0.75f, 0.6f);
    [Tooltip("Ô lối vào so với góc trái-dưới của footprint: x, bề rộng; hàng dưới footprint (y = -1).")]
    public Vector2Int entryTile; public int entryWidth = 1;
    public bool blocksMovement = true;         // sprinkler: false (dùng trigger)
    [Header("Gameplay (đặt riêng, không phải dữ liệu hình ảnh)")]
    public ItemCost[] buildCost;

    /// Tọa độ ô (cell) bị chiếm khi đặt tại ô gốc (góc trái-dưới).
    public System.Collections.Generic.IEnumerable<Vector2Int> OccupiedCells(Vector2Int origin)
    { for (int x = 0; x < footprintTiles.x; x++) for (int y = 0; y < footprintTiles.y; y++) yield return origin + new Vector2Int(x, y); }
}
