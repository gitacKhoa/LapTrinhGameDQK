using Core;
using UnityEngine;
using UnityEngine.Rendering.Universal;

[RequireComponent(typeof(Light2D))]
public class DayNightLight : MonoBehaviour
{
    [Header("Color By Time")]
    [SerializeField] private Color morningColor = new Color(1f, 0.77f, 0.55f);   // 06:00 hơi cam
    [SerializeField] private Color noonColor = Color.white;                         // 12:00 trắng
    [SerializeField] private Color eveningColor = new Color(1f, 0.48f, 0.20f);  // 18:00 cam đậm
    [SerializeField] private Color nightColor = new Color(0.09f, 0.13f, 0.23f);   // 20:00+ xanh đen

    [Header("Intensity By Time")]
    [SerializeField] private float morningIntensity = 0.85f;
    [SerializeField] private float noonIntensity = 1.0f;
    [SerializeField] private float eveningIntensity = 0.75f;
    [SerializeField] private float nightIntensity = 0.35f;

    private Light2D globalLight;

    private void Awake()
    {
        globalLight = GetComponent<Light2D>();
    }

    private void Update()
    {
        if (TimeManager.Instance == null || globalLight == null) return;

        float t = TimeManager.Instance.TotalHours; // 0.0 -> 24.0
        EvaluateLighting(t, out Color targetColor, out float targetIntensity);

        globalLight.color = targetColor;
        globalLight.intensity = targetIntensity;
    }

    private void EvaluateLighting(float hour, out Color col, out float intensity)
    {
        if (hour < 6f)
        {
            // Đêm khuya đến trước 06:00: giữ xanh đen, chuyển dần sang sáng lúc gần 6:00
            float k = Mathf.InverseLerp(5f, 6f, hour);
            col = Color.Lerp(nightColor, morningColor, k);
            intensity = Mathf.Lerp(nightIntensity, morningIntensity, k);
        }
        else if (hour < 12f)
        {
            // 06:00 -> 12:00: hơi cam -> trắng giữa ngày
            float k = Mathf.InverseLerp(6f, 12f, hour);
            col = Color.Lerp(morningColor, noonColor, k);
            intensity = Mathf.Lerp(morningIntensity, noonIntensity, k);
        }
        else if (hour < 18f)
        {
            // 12:00 -> 18:00: trắng -> cam đậm hoàng hôn
            float k = Mathf.InverseLerp(12f, 18f, hour);
            col = Color.Lerp(noonColor, eveningColor, k);
            intensity = Mathf.Lerp(noonIntensity, eveningIntensity, k);
        }
        else if (hour < 20f)
        {
            // 18:00 -> 20:00: cam đậm -> xanh đen ban đêm
            float k = Mathf.InverseLerp(18f, 20f, hour);
            col = Color.Lerp(eveningColor, nightColor, k);
            intensity = Mathf.Lerp(eveningIntensity, nightIntensity, k);
        }
        else
        {
            // Từ 20:00 trở đi: xanh đen
            col = nightColor;
            intensity = nightIntensity;
        }
    }
}