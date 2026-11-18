using System;
using UnityEngine;

public class GridManager : MonoBehaviour
{
    private Grid grid;
    [SerializeField] public GameObject gridPrefab;
    [SerializeField] public Vector3 worldPosition;
    void Start()
    {
        Console.WriteLine("Hello World");
        gridPrefab = GameObject.Find("Grid");
        grid = gridPrefab.GetComponent<Grid>();
        
    }

    private void Update()
    {
        if (Input.GetMouseButtonDown(0))
        {
            Vector3 mousePosition = Input.mousePosition;
            Vector3 worldPosition = Camera.main.ScreenToWorldPoint(mousePosition);
            Vector3Int cellPosition = grid.WorldToCell(worldPosition);
            Debug.Log($"Mouse Position: {mousePosition} → World Position: {worldPosition} → Cell Position: {cellPosition}");
        }
    }
}


