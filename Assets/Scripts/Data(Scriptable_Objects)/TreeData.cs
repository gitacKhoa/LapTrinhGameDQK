using UnityEngine;

[CreateAssetMenu(menuName = "Game/Tree Data")]
public class TreeDefinition : ScriptableObject
{
    public string treeName;

    public int maxHealth;

    public Vector2Int footprintSize;

    public Sprite[] growthSprites;
}