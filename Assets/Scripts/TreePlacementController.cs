using System.Collections.Generic;
using UnityEngine;

public class TreePlacementController : MonoBehaviour
{
    [Header("References")]
    [SerializeField] private Grid grid;
    [SerializeField] private Camera mainCamera;

    [Header("Tree Prefabs")]
    [SerializeField] private GameObject[] treePrefabs;

    [Header("Placement")]
    [SerializeField] private int selectedTreeIndex = 0;

    // Lưu các cell đã có cây
    private HashSet<Vector3Int> occupiedCells = new HashSet<Vector3Int>();

    void Update()
    {
        if (Input.GetMouseButtonDown(0))
        {
            PlaceTree();
        }

        // Chọn cây bằng phím 1, 2, 3...
        for (int i = 0; i < treePrefabs.Length && i < 9; i++)
        {
            if (Input.GetKeyDown(KeyCode.Alpha1 + i))
            {
                selectedTreeIndex = i;
            }
        }
    }

    void PlaceTree()
    {
        if (treePrefabs.Length == 0 || grid == null)
            return;

        Vector3 mouseWorld = mainCamera.ScreenToWorldPoint(
            Input.mousePosition
        );

        Vector3Int cell = grid.WorldToCell(mouseWorld);

        // Kiểm tra ô đã có cây chưa
        if (occupiedCells.Contains(cell))
            return;

        Vector3 spawnPosition = grid.GetCellCenterWorld(cell);

        GameObject tree = Instantiate(
            treePrefabs[selectedTreeIndex],
            spawnPosition,
            Quaternion.identity
        );
        
        tree.name = treePrefabs[selectedTreeIndex].name;

        occupiedCells.Add(cell);
    }
}