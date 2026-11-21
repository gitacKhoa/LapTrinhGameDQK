using Core;
using TMPro;
using UnityEngine;

public class SimpleClockUI : MonoBehaviour
{
    [SerializeField] private TMP_Text timeText;
    [SerializeField] private bool showDay = true;
    [SerializeField] private string dayPrefix = "Day ";

    private void OnEnable()
    {
        BindEvents();
        Refresh();
    }

    private void Start()
    {
        BindEvents();
        Refresh();
    }

    private void OnDisable()
    {
        if (TimeManager.Instance == null) return;
        TimeManager.Instance.OnMinuteChanged -= HandleTimeChanged;
        TimeManager.Instance.OnDayStarted -= HandleDayChanged;
    }

    private void BindEvents()
    {
        if (TimeManager.Instance == null) return;
        TimeManager.Instance.OnMinuteChanged -= HandleTimeChanged;
        TimeManager.Instance.OnDayStarted -= HandleDayChanged;
        TimeManager.Instance.OnMinuteChanged += HandleTimeChanged;
        TimeManager.Instance.OnDayStarted += HandleDayChanged;
    }

    private void HandleTimeChanged(int hour, int minute)
    {
        if (timeText == null) return;

        string formattedTime = $"{hour:00}:{minute:00}";
        if (showDay && TimeManager.Instance != null)
        {
            timeText.text = $"{dayPrefix}{TimeManager.Instance.Day} - {formattedTime}";
        }
        else
        {
            timeText.text = formattedTime;
        }
    }

    private void HandleDayChanged(int day)
    {
        if (TimeManager.Instance == null) return;
        HandleTimeChanged(TimeManager.Instance.Hour, TimeManager.Instance.Minute);
    }

    private void Refresh()
    {
        if (TimeManager.Instance == null) return;
        HandleTimeChanged(TimeManager.Instance.Hour, TimeManager.Instance.Minute);
    }
}