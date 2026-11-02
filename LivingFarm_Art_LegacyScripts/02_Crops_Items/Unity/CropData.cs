using System;
using UnityEngine;

[Flags] public enum Season { None = 0, Spring = 1, Summer = 2, Autumn = 4, Winter = 8 }

[CreateAssetMenu(menuName = "Living Farm/Crop Data", fileName = "Crop_")]
public class CropData : ScriptableObject
{
    public string id;
    public string displayName;
    public ItemData seedItem;
    public ItemData harvestItem;
    public Season growSeasons = Season.Spring;

    [Header("Sinh trưởng")]
    [Tooltip("Số ngày ở mỗi giai đoạn 0..3 (seed, sprout, growing, mature). Sau đó cây 'ready'.")]
    public int[] daysPerStage = { 1, 1, 2, 2 };
    public bool regrows;
    [Min(1)] public int regrowDays = 3;
    public Vector2Int harvestYield = new Vector2Int(1, 1);

    [Header("Sprite: seed, sprout, growing, mature, ready")]
    public Sprite[] stageSprites = new Sprite[5];
    public Sprite wiltedSprite;

    public int TotalDaysToReady { get { int t = 0; foreach (var d in daysPerStage) t += d; return t; } }

    public Sprite GetSprite(int daysGrown, bool wilted)
    {
        if (wilted) return wiltedSprite;
        int stage = 0, acc = 0;
        for (; stage < daysPerStage.Length; stage++)
        {
            acc += daysPerStage[stage];
            if (daysGrown < acc) break;
        }
        return stageSprites[Mathf.Min(stage, stageSprites.Length - 1)];
    }

    void OnValidate()
    {
        if (daysPerStage == null || daysPerStage.Length != 4) Array.Resize(ref daysPerStage, 4);
        if (stageSprites == null || stageSprites.Length != 5) Array.Resize(ref stageSprites, 5);
    }
}
