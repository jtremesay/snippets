using UnityEngine;
using System.Collections;


public enum ScaleType {
    kCrop,
    kInside
}
    
class Texture2DHelpers {
    public static Texture2D rescaleCenter(Texture2D srcTexture, Vector2 destSize, ScaleType scaleType) {
        var srcSize = new Vector2(
            srcTexture.width, 
            srcTexture.height);
        var scale = Texture2DHelpers.scaleFactor(
            srcSize,
            destSize,
            scaleType);
        var scaledSize = srcSize * scale;
        

        // Convert float values to int
        var srcWidth = srcTexture.width;
        var scaledWidth = (int) scaledSize.x;
        var scaledHeight = (int) scaledSize.y;
        var destWidth = (int) destSize.x;
        var destHeight = (int) destSize.y;
        

        var minX = Helpers.clamp((destWidth - scaledWidth) / 2, 0, destWidth - 1);
        var maxX = destWidth - 1 - minX;
        var minY = Helpers.clamp((destHeight - scaledHeight) / 2, 0, destHeight - 1);
        var maxY = destHeight - 1 - minY;
        
            
        var srcPixels = srcTexture.GetPixels();
        var destPixels = new Color[destWidth * destHeight];
        for (var destX=0; destX < destWidth; ++destX) {
            for (var destY=0; destY < destHeight; ++destY) {
                Color destPixel;                
                if (destX >= minX && destX <= maxX && destY >= minY && destY <= maxY) {
                    var scaledX = destX - minX;
                    var scaledY = destY - minY;
                    
                    var srcX = (int) (scaledX / scale);
                    var srcY = (int) (scaledY / scale);
                    
                    var srcOffset = srcY * srcWidth + srcX;
                    destPixel = srcPixels[srcOffset];
                } else {
                    destPixel = fillColor;
                }
                
                var destOffset = destY * destWidth + destX;
                destPixels[destOffset] = destPixel;
            }
        }
        
        var destTexture = new Texture2D(destWidth, destHeight); 
        destTexture.SetPixels(destPixels);
        destTexture.Apply();
        return destTexture; 
    }

    public static float scaleFactor(Vector2 srcSize, Vector2 destSize, ScaleType scaleType) {
        var scaleX = destSize.x / srcSize.x;
        var scaleY = destSize.y / srcSize.y;
        float scale;
        switch (scaleType) {
        case ScaleType.kCrop:
            scale = Mathf.Max(scaleX, scaleY);
            break;
            
        case ScaleType.kInside:
            scale = Mathf.Min(scaleX, scaleY);
            break;
            
        default:
            Debug.LogWarning("unknow scale type");
            scale = 1.0f;
            break;
        }
        
        return scale;
    }
}