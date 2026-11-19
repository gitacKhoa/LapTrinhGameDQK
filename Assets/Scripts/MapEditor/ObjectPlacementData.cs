
using UnityEngine;

public class ObjectPlacementData : MonoBehaviour
{
    [Header("Footprint")]
    [Min(1)]
    public int width = 1;

    [Min(1)]
    public int height = 1;

    [Header("Placement")]
    public Vector3 visualOffset = Vector3.zero;

    // Logical position: bottom-left cell of footprint
    [HideInInspector]
    public Vector3Int bottomLeftCell;

    [HideInInspector]
    public bool hasPlacementCell;
}
