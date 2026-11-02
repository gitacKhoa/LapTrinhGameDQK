using UnityEngine;

/// Đổi sprite theo trạng thái máy (idle / working / ready). Không cần Animator.
/// Gán mảng sprite theo thứ tự cắt từ machines_sheet: [idle, work_a, work_b, ready].
[RequireComponent(typeof(SpriteRenderer))]
public class MachineAnimator : MonoBehaviour
{
    public enum State { Idle, Working, Ready }
    public Sprite[] frames = new Sprite[4];
    public float workFps = 4f;
    public State state = State.Idle;
    SpriteRenderer sr;

    void Awake() => sr = GetComponent<SpriteRenderer>();
    void Update()
    {
        if (frames == null || frames.Length < 4 || frames[0] == null) return;
        sr.sprite = state switch
        {
            State.Working => frames[1 + (int)(Time.time * workFps) % 2],
            State.Ready => frames[3],
            _ => frames[0]
        };
    }
}
