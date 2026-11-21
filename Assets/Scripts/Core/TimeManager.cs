using System;
using UnityEngine;

namespace Core
{
    public class TimeManager : MonoBehaviour
    {
        public static TimeManager Instance { get; private set; }

        [Header("Time Settings")]
        [Tooltip("1 giờ game = 10 phút thật (600s) -> 1 phút game = 10s thật")]
        [SerializeField] private float realSecondsPerGameMinute = 10f;

        [Header("Start Time")]
        [SerializeField] private int startDay = 1;
        [SerializeField] private int startHour = 6;
        [SerializeField] private int startMinute = 0;

        public int Day { get; private set; }
        public int Hour { get; private set; }
        public int Minute { get; private set; }

        /// <summary>Giá trị thời gian liên tục (ví dụ 6.5 = 6:30, 18.0 = 18:00) để nội suy mượt mà.</summary>
        public float TotalHours => Hour + (Minute / 60f);

        /// <summary>Cờ tạm dừng thời gian (dùng khi mở menu hoặc tạm dừng game).</summary>
        public bool IsPaused { get; set; }

        public event Action<int, int> OnMinuteChanged; // (hour, minute)
        public event Action<int> OnHourChanged;       // (hour)
        public event Action<int> OnDayStarted;        // (day)
        public event Action<int> OnDayEnded;          // (day)

        private float minuteTimer;

        private void Awake()
        {
            if (Instance != null && Instance != this)
            {
                Destroy(gameObject);
                return;
            }
            Instance = this;
        }

        private void Start()
        {
            Day = startDay;
            Hour = startHour;
            Minute = startMinute;
            minuteTimer = 0f;

            OnDayStarted?.Invoke(Day);
            OnHourChanged?.Invoke(Hour);
            OnMinuteChanged?.Invoke(Hour, Minute);
        }

        private void Update()
        {
            if (IsPaused) return;

            minuteTimer += Time.deltaTime;
            while (minuteTimer >= realSecondsPerGameMinute)
            {
                minuteTimer -= realSecondsPerGameMinute;
                AdvanceOneMinute();
            }
        }

        private void AdvanceOneMinute()
        {
            Minute++;
            if (Minute >= 60)
            {
                Minute = 0;
                Hour++;

                if (Hour >= 24)
                {
                    EndDay();
                    return;
                }

                OnHourChanged?.Invoke(Hour);
            }

            OnMinuteChanged?.Invoke(Hour, Minute);
        }

        /// <summary>Kết thúc ngày hiện tại và bắt đầu ngày mới lúc 06:00.</summary>
        public void EndDay()
        {
            OnDayEnded?.Invoke(Day);

            Day++;
            Hour = 6;
            Minute = 0;
            minuteTimer = 0f;

            OnDayStarted?.Invoke(Day);
            OnHourChanged?.Invoke(Hour);
            OnMinuteChanged?.Invoke(Hour, Minute);
        }

        public void SetPaused(bool paused)
        {
            IsPaused = paused;
        }

        public string GetFormattedTime() => $"{Hour:00}:{Minute:00}";
        public string GetFormattedDay() => $"Day {Day}";
    }
}