using System.Collections;
using UnityEngine;

[RequireComponent(typeof(Rigidbody2D))]
[RequireComponent(typeof(Animator))]
public class NPCWander : MonoBehaviour
{
    public enum Anim { Idle, Walk, Eat }
    public enum Dir { Down, Up, Left, Right }

    [Header("Wander Settings")]
    [SerializeField] private float moveSpeed = 2f;
    [SerializeField] private float wanderRadius = 3f; 
    [SerializeField] private float minIdleTime = 2f; 
    [SerializeField] private float maxIdleTime = 5f; 

    private Rigidbody2D rb;
    private Animator anim;
    private Vector2 startPosition;
    private Vector2 targetPosition;
    private Dir facing = Dir.Down;

    void Awake()
    {
        rb = GetComponent<Rigidbody2D>();
        anim = GetComponent<Animator>();
    }

    void Start()
    {
        startPosition = transform.position;
        StartCoroutine(WanderRoutine());
    }

    IEnumerator WanderRoutine()
    {
        while (true)
        {
            // --- GIAI ĐOẠN 1: ĐỨNG YÊN (IDLE) ---
            rb.linearVelocity = Vector2.zero;
            ApplyAnimation(Vector2.zero);

            float idleDuration = Random.Range(minIdleTime, maxIdleTime);
            yield return new WaitForSeconds(idleDuration);

            // --- GIAI ĐOẠN 2: CHỌN ĐIỂM ĐẾN MỚI ---
            Vector2 randomOffset = Random.insideUnitCircle * wanderRadius;
            targetPosition = startPosition + randomOffset;

            // --- GIAI ĐOẠN 3: DI CHUYỂN ĐẾN ĐÍCH ---
            // Thêm giới hạn thời gian di chuyển (timeout) tối đa 5 giây để tránh việc NPC bị kẹt vật cản mà cứ cố đi mãi
            float timer = 0f;
            float maxTravelTime = 5f; 

            while (Vector2.Distance(transform.position, targetPosition) > 0.2f && timer < maxTravelTime)
            {
                timer += Time.deltaTime;
                Vector2 direction = (targetPosition - (Vector2)transform.position).normalized;

                // Di chuyển vật lý
                rb.linearVelocity = direction * moveSpeed;

                // Chỉ cập nhật hướng nhìn nếu lực di chuyển thực sự đáng kể (tránh nhiễu số thập phân)
                if (direction.sqrMagnitude > 0.05f)
                {
                    UpdateFacingDirection(direction);
                }

                ApplyAnimation(direction);
                yield return null;
            }
        }
    }

    void UpdateFacingDirection(Vector2 move)
    {
        // Dùng độ chênh lệch rõ ràng hơn để tránh bị đổi hướng ngẫu nhiên khi đi chéo nhẹ
        if (Mathf.Abs(move.x) > Mathf.Abs(move.y))
        {
            facing = move.x < 0 ? Dir.Left : Dir.Right;
        }
        else
        {
            facing = move.y < 0 ? Dir.Down : Dir.Up;
        }
    }

    void ApplyAnimation(Vector2 move)
    {
        bool isMoving = move.sqrMagnitude > 0.05f;
        int animIndex = isMoving ? (int)Anim.Walk : (int)Anim.Idle;

        if (anim != null)
        {
            anim.SetInteger("Anim", animIndex);
            anim.SetFloat("Dir", (float)facing);
        }
    }
}