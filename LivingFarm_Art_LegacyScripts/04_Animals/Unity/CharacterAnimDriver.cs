using System.Collections;
using UnityEngine;

/// Gắn cùng Animator + SpriteRenderer (+ Rigidbody2D). Giá trị Anim/Dir khớp LivingFarmAnimBuilder.
[RequireComponent(typeof(Animator))]
public class CharacterAnimDriver : MonoBehaviour
{
    public enum Anim { Idle, Walk, Hoe, Water, Harvest, Chop, Mine, CarryIdle, CarryWalk, Eat }
    public enum Dir { Down, Up, Left, Right }

    Animator anim; Dir facing = Dir.Down; bool busy;
    void Awake() => anim = GetComponent<Animator>();

    /// Gọi mỗi frame từ script di chuyển.
    public void SetMovement(Vector2 move, bool carrying = false)
    {
        if (busy) return;
        if (move.sqrMagnitude > 0.01f)
            facing = Mathf.Abs(move.x) > Mathf.Abs(move.y) ? (move.x < 0 ? Dir.Left : Dir.Right) : (move.y < 0 ? Dir.Down : Dir.Up);
        var a = move.sqrMagnitude > 0.01f ? (carrying ? Anim.CarryWalk : Anim.Walk) : (carrying ? Anim.CarryIdle : Anim.Idle);
        Apply(a);
    }

    /// Chơi animation hành động (cuốc, tưới...) một lần rồi quay lại idle. Thời lượng = số frame / fps.
    public IEnumerator PlayAction(Anim action, float duration)
    {
        busy = true; Apply(action);
        yield return new WaitForSeconds(duration);
        busy = false; Apply(Anim.Idle);
    }

    public Vector2 FacingVector => facing switch { Dir.Down => Vector2.down, Dir.Up => Vector2.up, Dir.Left => Vector2.left, _ => Vector2.right };
    void Apply(Anim a) { anim.SetInteger("Anim", (int)a); anim.SetInteger("Dir", (int)facing); }
}
