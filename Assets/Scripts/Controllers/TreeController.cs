using UnityEngine;

public class TreeController : MonoBehaviour
{
    public TreeData data;

    public int currentHealth;

    public int growthStage;

    private void Start()
    {
        currentHealth = data.maxHealth;
    }
}