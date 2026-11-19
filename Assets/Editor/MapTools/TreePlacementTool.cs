
using System;
using System.Collections.Generic;
using UnityEditor;
using UnityEngine;

public class ObjectPlacementTool : EditorWindow
{
    private enum PlacementMode
    {
        RandomClick,
        RandomScatter
    }

    private Grid grid;
    private Transform objectsParent;

    private List<GameObject> prefabPool = new();

    private PlacementMode mode = PlacementMode.RandomClick;
    private bool isPlacing;

    private GameObject previewObject;
    private SpriteRenderer[] previewRenderers;
    private GameObject previewSourcePrefab;

    private GameObject currentPrefab;
    private Vector3Int currentCell;
    private Vector3Int footprintBottomLeft;
    private bool currentPlacementValid;

    private readonly HashSet<Vector3Int> occupiedCells = new();

    // Random settings
    private int randomSeed = 12345;
    private System.Random random;

    // Scatter settings
    private int scatterCount = 30;
    private int maxAttemptsMultiplier = 50;

    private bool isSelectingArea;
    private Vector3Int scatterStartCell;
    private Vector3Int scatterEndCell;

    [MenuItem("Tools/Map Editor/Object Placement")]
    public static void Open()
    {
        GetWindow<ObjectPlacementTool>("Object Placement");
    }

    private void OnEnable()
    {
        SceneView.duringSceneGui += OnSceneGUI;
        ResetRandom();
    }

    private void OnDisable()
    {
        SceneView.duringSceneGui -= OnSceneGUI;
        DestroyPreview();
    }

    private void OnGUI()
    {
        GUILayout.Label("Object Placement Tool", EditorStyles.boldLabel);

        grid = (Grid)EditorGUILayout.ObjectField(
            "Grid", grid, typeof(Grid), true);

        objectsParent = (Transform)EditorGUILayout.ObjectField(
            "Objects Root", objectsParent, typeof(Transform), true);

        EditorGUILayout.Space(8);

        DrawPrefabPool();

        EditorGUILayout.Space(8);

        GUILayout.Label("Placement Mode", EditorStyles.boldLabel);

        PlacementMode newMode = (PlacementMode)EditorGUILayout.EnumPopup(
            "Mode", mode);

        if (newMode != mode)
        {
            mode = newMode;
            isSelectingArea = false;
            DestroyPreview();
            Repaint();
        }

        EditorGUILayout.Space(5);

        randomSeed = EditorGUILayout.IntField("Random Seed", randomSeed);

        if (mode == PlacementMode.RandomScatter)
        {
            scatterCount = Mathf.Max(
                1,
                EditorGUILayout.IntField("Object Count", scatterCount)
            );
        }

        EditorGUILayout.Space(8);

        GUI.enabled = CanStart();

        if (GUILayout.Button(
            isPlacing ? "Stop Placement" : "Start Placement"))
        {
            isPlacing = !isPlacing;

            if (isPlacing)
            {
                ResetRandom();

                if (mode == PlacementMode.RandomClick)
                    ChooseNextPrefab();
            }
            else
            {
                DestroyPreview();
                isSelectingArea = false;
            }

            SceneView.RepaintAll();
        }

        GUI.enabled = true;

        if (isPlacing)
        {
            if (mode == PlacementMode.RandomClick)
            {
                EditorGUILayout.HelpBox(
                    "Random Click:\n" +
                    "Move mouse to preview.\n" +
                    "Left-click = place random prefab.\n" +
                    "ESC = stop.",
                    MessageType.Info
                );
            }
            else
            {
                EditorGUILayout.HelpBox(
                    "Random Scatter:\n" +
                    "Left-click and drag to select an area.\n" +
                    "Release mouse to scatter objects.\n" +
                    "ESC = stop.",
                    MessageType.Info
                );
            }
        }
    }

    private void DrawPrefabPool()
    {
        GUILayout.Label("Prefab Pool", EditorStyles.boldLabel);

        for (int i = 0; i < prefabPool.Count; i++)
        {
            EditorGUILayout.BeginHorizontal();

            prefabPool[i] = (GameObject)EditorGUILayout.ObjectField(
                prefabPool[i],
                typeof(GameObject),
                false
            );

            if (GUILayout.Button("X", GUILayout.Width(25)))
            {
                prefabPool.RemoveAt(i);
                i--;
            }

            EditorGUILayout.EndHorizontal();
        }

        if (GUILayout.Button("+ Add Prefab"))
            prefabPool.Add(null);
    }

    private bool CanStart()
    {
        if (grid == null || objectsParent == null)
            return false;

        foreach (GameObject prefab in prefabPool)
        {
            if (prefab != null)
                return true;
        }

        return false;
    }

    private void ResetRandom()
    {
        random = new System.Random(randomSeed);
    }

    private GameObject GetRandomPrefab()
    {
        List<GameObject> validPrefabs = new();

        foreach (GameObject prefab in prefabPool)
        {
            if (prefab != null)
                validPrefabs.Add(prefab);
        }

        if (validPrefabs.Count == 0)
            return null;

        return validPrefabs[random.Next(validPrefabs.Count)];
    }

    private void ChooseNextPrefab()
    {
        GameObject nextPrefab = GetRandomPrefab();

        if (nextPrefab != currentPrefab)
            DestroyPreview();

        currentPrefab = nextPrefab;
    }

    private void OnSceneGUI(SceneView sceneView)
    {
        if (!isPlacing ||
            grid == null ||
            objectsParent == null)
            return;

        Event e = Event.current;

        if (e.alt)
            return;

        int controlID = GUIUtility.GetControlID(FocusType.Passive);
        HandleUtility.AddDefaultControl(controlID);

        if (e.type == EventType.KeyDown &&
            e.keyCode == KeyCode.Escape)
        {
            isPlacing = false;
            isSelectingArea = false;
            DestroyPreview();

            Repaint();
            e.Use();
            return;
        }

        if (!TryGetMouseCell(e.mousePosition, out currentCell))
            return;

        if (mode == PlacementMode.RandomClick)
            HandleRandomClick(sceneView, e);
        else
            HandleRandomScatter(sceneView, e);

        sceneView.Repaint();
    }

    private bool TryGetMouseCell(
        Vector2 mousePosition,
        out Vector3Int cell)
    {
        Ray ray = HandleUtility.GUIPointToWorldRay(mousePosition);

        Plane plane = new Plane(
            grid.transform.forward,
            grid.transform.position
        );

        if (plane.Raycast(ray, out float distance))
        {
            Vector3 world = ray.GetPoint(distance);
            cell = grid.WorldToCell(world);
            return true;
        }

        cell = Vector3Int.zero;
        return false;
    }

    // --------------------------------------------------
    // RANDOM CLICK
    // --------------------------------------------------

    private void HandleRandomClick(SceneView sceneView, Event e)
    {
        if (currentPrefab == null)
            ChooseNextPrefab();

        if (currentPrefab == null)
            return;

        GetPrefabFootprint(
            currentPrefab,
            out int width,
            out int height,
            out Vector3 visualOffset
        );

        footprintBottomLeft = GetFootprintBottomLeft(
            currentCell,
            width,
            height
        );

        RebuildOccupiedCells();

        currentPlacementValid = IsFootprintFree(
            footprintBottomLeft,
            width,
            height
        );

        Vector3 previewPosition =
            GetFootprintCenterWorld(
                footprintBottomLeft,
                width,
                height
            ) + visualOffset;

        UpdatePreview(previewPosition, currentPlacementValid);

        DrawFootprint(
            footprintBottomLeft,
            width,
            height,
            currentPlacementValid
        );

        if (e.type == EventType.MouseDown &&
            e.button == 0)
        {
            if (currentPlacementValid)
            {
                PlacePrefab(
                    currentPrefab,
                    footprintBottomLeft,
                    width,
                    height
                );

                // Update occupied cells immediately
                AddFootprintToOccupied(
                    footprintBottomLeft,
                    width,
                    height
                );

                ChooseNextPrefab();
            }

            e.Use();
        }
    }

    // --------------------------------------------------
    // RANDOM SCATTER
    // --------------------------------------------------

    private void HandleRandomScatter(SceneView sceneView, Event e)
    {
        if (e.type == EventType.MouseDown && e.button == 0)
        {
            scatterStartCell = currentCell;
            scatterEndCell = currentCell;
            isSelectingArea = true;

            e.Use();
        }

        if (isSelectingArea &&
            (e.type == EventType.MouseDrag ||
             e.type == EventType.MouseMove))
        {
            scatterEndCell = currentCell;
            e.Use();
        }

        if (isSelectingArea)
        {
            scatterEndCell = currentCell;

            DrawSelectionArea(
                scatterStartCell,
                scatterEndCell
            );
        }

        if (e.type == EventType.MouseUp &&
            e.button == 0 &&
            isSelectingArea)
        {
            scatterEndCell = currentCell;
            isSelectingArea = false;

            ScatterObjects(
                scatterStartCell,
                scatterEndCell
            );

            e.Use();
        }
    }

    private void ScatterObjects(
        Vector3Int startCell,
        Vector3Int endCell)
    {
        RebuildOccupiedCells();

        int minX = Mathf.Min(startCell.x, endCell.x);
        int maxX = Mathf.Max(startCell.x, endCell.x);

        int minY = Mathf.Min(startCell.y, endCell.y);
        int maxY = Mathf.Max(startCell.y, endCell.y);

        int placedCount = 0;

        int maxAttempts = Mathf.Max(
            100,
            scatterCount * maxAttemptsMultiplier
        );

        for (int attempt = 0;
             attempt < maxAttempts && placedCount < scatterCount;
             attempt++)
        {
            GameObject prefab = GetRandomPrefab();

            if (prefab == null)
                break;

            GetPrefabFootprint(
                prefab,
                out int width,
                out int height,
                out Vector3 visualOffset
            );

            // Pick a random mouse cell inside the selected area
            int randomX = random.Next(minX, maxX + 1);
            int randomY = random.Next(minY, maxY + 1);

            Vector3Int mouseCell = new Vector3Int(
                randomX,
                randomY,
                startCell.z
            );

            Vector3Int bottomLeft = GetFootprintBottomLeft(
                mouseCell,
                width,
                height
            );

            // Ensure the whole footprint stays inside the area
            if (bottomLeft.x < minX ||
                bottomLeft.y < minY ||
                bottomLeft.x + width - 1 > maxX ||
                bottomLeft.y + height - 1 > maxY)
                continue;

            if (!IsFootprintFree(bottomLeft, width, height))
                continue;

            PlacePrefab(prefab, bottomLeft, width, height);

            // Prevent later objects from overlapping this one
            AddFootprintToOccupied(bottomLeft, width, height);

            placedCount++;
        }

        Debug.Log(
            $"Random Scatter completed: {placedCount}/{scatterCount} objects placed."
        );

        SceneView.RepaintAll();
    }

    // --------------------------------------------------
    // FOOTPRINT
    // --------------------------------------------------

    private void GetPrefabFootprint(
        GameObject prefab,
        out int width,
        out int height,
        out Vector3 visualOffset)
    {
        ObjectPlacementData data =
            prefab.GetComponent<ObjectPlacementData>();

        width = data != null ? Mathf.Max(1, data.width) : 1;
        height = data != null ? Mathf.Max(1, data.height) : 1;

        visualOffset = data != null
            ? data.visualOffset
            : Vector3.zero;
    }

    private Vector3Int GetFootprintBottomLeft(
        Vector3Int mouseCell,
        int width,
        int height)
    {
        int offsetX = width % 2 == 1 ? width / 2 : 0;
        int offsetY = height % 2 == 1 ? height / 2 : 0;

        return mouseCell - new Vector3Int(offsetX, offsetY, 0);
    }

    private Vector3 GetFootprintCenterWorld(
        Vector3Int bottomLeft,
        int width,
        int height)
    {
        Vector3 center = grid.GetCellCenterWorld(bottomLeft);

        center += new Vector3(
            (width - 1) * 0.5f * grid.cellSize.x,
            (height - 1) * 0.5f * grid.cellSize.y,
            0
        );

        center.z = grid.transform.position.z;

        return center;
    }

    private bool IsFootprintFree(
        Vector3Int bottomLeft,
        int width,
        int height)
    {
        for (int x = 0; x < width; x++)
        {
            for (int y = 0; y < height; y++)
            {
                Vector3Int cell = bottomLeft +
                    new Vector3Int(x, y, 0);

                if (occupiedCells.Contains(cell))
                    return false;
            }
        }

        return true;
    }

    private void AddFootprintToOccupied(
        Vector3Int bottomLeft,
        int width,
        int height)
    {
        for (int x = 0; x < width; x++)
        {
            for (int y = 0; y < height; y++)
            {
                occupiedCells.Add(
                    bottomLeft + new Vector3Int(x, y, 0)
                );
            }
        }
    }

    private void RebuildOccupiedCells()
    {
        occupiedCells.Clear();

        ObjectPlacementData[] placedObjects =
            objectsParent.GetComponentsInChildren<ObjectPlacementData>(true);

        foreach (ObjectPlacementData data in placedObjects)
        {
            if (data == null ||
                !data.gameObject.scene.IsValid())
                continue;

            if ((data.gameObject.hideFlags &
                 HideFlags.HideAndDontSave) != 0)
                continue;

            int width = Mathf.Max(1, data.width);
            int height = Mathf.Max(1, data.height);

            Vector3Int bottomLeft;

            if (data.hasPlacementCell)
            {
                bottomLeft = data.bottomLeftCell;
            }
            else
            {
                // Fallback for objects placed before this version
                Vector3 offset = new Vector3(
                    (width - 1) * 0.5f * grid.cellSize.x,
                    (height - 1) * 0.5f * grid.cellSize.y,
                    0
                );

                Vector3 bottomLeftWorld =
                    data.transform.position
                    - data.visualOffset
                    - offset;

                bottomLeft = grid.WorldToCell(bottomLeftWorld);
            }

            AddFootprintToOccupied(
                bottomLeft,
                width,
                height
            );
        }
    }

    // --------------------------------------------------
    // PLACE OBJECT
    // --------------------------------------------------

    private void PlacePrefab(
        GameObject prefab,
        Vector3Int bottomLeft,
        int width,
        int height)
    {
        GameObject instance = (GameObject)PrefabUtility.InstantiatePrefab(
            prefab
        );

        if (instance == null)
            return;

        ObjectPlacementData data =
            instance.GetComponent<ObjectPlacementData>();

        Vector3 visualOffset = data != null
            ? data.visualOffset
            : Vector3.zero;

        instance.transform.SetParent(objectsParent);

        instance.transform.position =
            GetFootprintCenterWorld(bottomLeft, width, height)
            + visualOffset;

        if (data != null)
        {
            data.bottomLeftCell = bottomLeft;
            data.hasPlacementCell = true;
        }

        instance.name =
            prefab.name + "_" + bottomLeft.x + "_" + bottomLeft.y;

        Undo.RegisterCreatedObjectUndo(
            instance,
            "Place Object"
        );
    }

    // --------------------------------------------------
    // PREVIEW
    // --------------------------------------------------

    private void UpdatePreview(
        Vector3 position,
        bool isValid)
    {
        if (previewSourcePrefab != currentPrefab)
        {
            DestroyPreview();
            CreatePreview();
        }

        if (previewObject == null)
            CreatePreview();

        if (previewObject == null)
            return;

        previewObject.transform.position = position;

        Color color = isValid
            ? new Color(0.2f, 1f, 0.2f, 0.65f)
            : new Color(1f, 0.2f, 0.2f, 0.65f);

        foreach (SpriteRenderer sr in previewRenderers)
        {
            if (sr != null)
                sr.color = color;
        }
    }

    private void CreatePreview()
    {
        if (currentPrefab == null)
            return;

        previewObject = (GameObject)PrefabUtility.InstantiatePrefab(
            currentPrefab
        );

        if (previewObject == null)
            return;

        previewSourcePrefab = currentPrefab;
        previewObject.hideFlags = HideFlags.HideAndDontSave;

        foreach (MonoBehaviour behaviour in
                 previewObject.GetComponentsInChildren<MonoBehaviour>(true))
        {
            behaviour.enabled = false;
        }

        foreach (Collider2D col in
                 previewObject.GetComponentsInChildren<Collider2D>(true))
        {
            col.enabled = false;
        }

        foreach (Collider col in
                 previewObject.GetComponentsInChildren<Collider>(true))
        {
            col.enabled = false;
        }

        previewRenderers =
            previewObject.GetComponentsInChildren<SpriteRenderer>(true);
    }

    private void DestroyPreview()
    {
        if (previewObject != null)
            DestroyImmediate(previewObject);

        previewObject = null;
        previewRenderers = null;
        previewSourcePrefab = null;
    }

    // --------------------------------------------------
    // DRAWING
    // --------------------------------------------------

    private void DrawFootprint(
        Vector3Int bottomLeft,
        int width,
        int height,
        bool isValid)
    {
        Handles.color = isValid ? Color.green : Color.red;

        for (int x = 0; x < width; x++)
        {
            for (int y = 0; y < height; y++)
            {
                Vector3Int cell = bottomLeft +
                    new Vector3Int(x, y, 0);

                Vector3 center = grid.GetCellCenterWorld(cell);
                center.z = grid.transform.position.z;

                Handles.DrawWireCube(center, grid.cellSize);
            }
        }
    }

    private void DrawSelectionArea(
        Vector3Int start,
        Vector3Int end)
    {
        Handles.color = Color.cyan;

        int minX = Mathf.Min(start.x, end.x);
        int maxX = Mathf.Max(start.x, end.x);
        int minY = Mathf.Min(start.y, end.y);
        int maxY = Mathf.Max(start.y, end.y);

        for (int x = minX; x <= maxX; x++)
        {
            for (int y = minY; y <= maxY; y++)
            {
                Vector3 center = grid.GetCellCenterWorld(
                    new Vector3Int(x, y, start.z)
                );

                center.z = grid.transform.position.z;

                Handles.DrawWireCube(center, grid.cellSize);
            }
        }

        Handles.Label(
            grid.GetCellCenterWorld(start),
            $"Area: {maxX - minX + 1} x {maxY - minY + 1}"
        );
    }
}
