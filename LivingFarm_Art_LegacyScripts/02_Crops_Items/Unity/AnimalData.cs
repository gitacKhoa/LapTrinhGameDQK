using UnityEngine;

[CreateAssetMenu(menuName = "Living Farm/Animal Data", fileName = "Animal_")]
public class AnimalData : ScriptableObject
{
    public string id;               // chicken, cow, sheep, duck
    public string displayName;
    public ItemData product;        // egg, milk, wool...
    [Min(1)] public int productIntervalDays = 1;
    public ItemData feedItem;
    public int buyPrice;
    public Sprite portrait;         // icon cửa hàng (bổ sung ở Giai đoạn 4)
    public RuntimeAnimatorController animator;  // gán ở Giai đoạn 4
}
