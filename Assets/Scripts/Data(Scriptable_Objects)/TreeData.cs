using UnityEngine;

[CreateAssetMenu(menuName = "Data/Tree")]
public class TreeData : ScriptableObject
{
    public string treeName;

    public int maxHealth;

    public Vector2Int footprintSize;

    public Sprite[] growthSprites;
}