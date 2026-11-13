// Assets/Editor/LivingFarmTexturePostprocessor.cs - CHƯA kiểm thử trong Unity 6000.3.11f1.
// Tự áp dụng thiết lập pixel art cho mọi texture dưới Assets/Art/ khi import (không đổi Sprite Mode / border / pivot).
using UnityEditor;
using UnityEngine;

public class LivingFarmTexturePostprocessor : AssetPostprocessor
{
    void OnPreprocessTexture()
    {
        if (!assetPath.StartsWith("Assets/Art/")) return;
        var imp = (TextureImporter)assetImporter;
        if (imp.textureType == TextureImporterType.Default) imp.textureType = TextureImporterType.Sprite;
        imp.filterMode = FilterMode.Point;
        imp.textureCompression = TextureImporterCompression.Uncompressed;
        imp.mipmapEnabled = false;
        imp.alphaIsTransparency = true;
        imp.npotScale = TextureImporterNPOTScale.None;
    }
}
