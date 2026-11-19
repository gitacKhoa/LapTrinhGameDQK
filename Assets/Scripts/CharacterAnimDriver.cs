using System.Collections;
using UnityEngine;
using UnityEngine.InputSystem;

[RequireComponent(typeof(Animator))]
[RequireComponent(typeof(Rigidbody2D))]
public class CharacterAnimDriver : MonoBehaviour
{
    public enum Anim { Idle, Walk, Hoe, Water, Harvest, Chop, Mine, CarryIdle, CarryWalk}
    public enum Dir { Down, Up, Left, Right }

    [Header("Movement Settings")]
    public float moveSpeed = 5f;

    Animator anim;
    Rigidbody2D rb;
    Dir facing = Dir.Down;
    bool busy;

    void Awake()
    {
        anim = GetComponent<Animator>();
        rb = GetComponent<Rigidbody2D>();
    }

    void Update()
    {
        if (busy) return;

        Vector2 moveInput = ReadMovementInput();
        SetMovement(moveInput);
    }

    void FixedUpdate()
    {
        if (busy)
        {
            if (rb != null) rb.linearVelocity = Vector2.zero;
            return;
        }

        Vector2 moveInput = ReadMovementInput();

        if (rb != null)
        {
            rb.linearVelocity = moveInput.normalized * moveSpeed;
        }
    }

    Vector2 ReadMovementInput()
    {
        float moveX = 0f;
        float moveY = 0f;

        if (Keyboard.current != null)
        {
            if (Keyboard.current.aKey.isPressed || Keyboard.current.leftArrowKey.isPressed) moveX = -1f;
            else if (Keyboard.current.dKey.isPressed || Keyboard.current.rightArrowKey.isPressed) moveX = 1f;

            if (Keyboard.current.sKey.isPressed || Keyboard.current.downArrowKey.isPressed) moveY = -1f;
            else if (Keyboard.current.wKey.isPressed || Keyboard.current.upArrowKey.isPressed) moveY = 1f;
        }

        return new Vector2(moveX, moveY);
    }

    public void SetMovement(Vector2 move, bool carrying = false)
    {
        if (busy) return;

        if (move.sqrMagnitude > 0.01f)
        {
            facing = Mathf.Abs(move.x) > Mathf.Abs(move.y)
                ? (move.x < 0 ? Dir.Left : Dir.Right)
                : (move.y < 0 ? Dir.Down : Dir.Up);
        }

        Anim a = move.sqrMagnitude > 0.01f
            ? (carrying ? Anim.CarryWalk : Anim.Walk)
            : (carrying ? Anim.CarryIdle : Anim.Idle);

        Apply(a);
    }

    public IEnumerator PlayAction(Anim action, float duration)
    {
        busy = true;
        if (rb != null) rb.linearVelocity = Vector2.zero;
        Apply(action);
        yield return new WaitForSeconds(duration);
        busy = false;
        Apply(Anim.Idle);
    }

    public Vector2 FacingVector => facing switch
    {
        Dir.Down => Vector2.down,
        Dir.Up => Vector2.up,
        Dir.Left => Vector2.left,
        _ => Vector2.right
    };

    void Apply(Anim a)
    {
        anim.SetInteger("Anim", (int)a);
        anim.SetFloat("Dir", (float)facing);
    }
}