# Express server

This is the express app that handles user-created diagrams from MyDraft app, which are exported into a JSON file in the following manner:

```
{
    animationScript: str,
    fileName: str,
    diagram: [{
        id: str,
        index: number,
        style: {
            colorBackround: number,
            size: str,              // `width height`
        },
    },],
    image: [{
        content: str,               // `image-url`
        diagram: str,               // `diagram-id`
        id: str,
        style: {
            keepAspectRatio: bool,
            position: str,          // `x-left y-top`
            size: str,              // `width height`
        },
    },],
    katex: [{
        content: str,               // `katex-code`
        diagram: str,               // `diagram-id`
        id: str,
        style: {
            alignment: str          // `left/center/right`
            colorForeground: number,
            fontSize: number,
            position: str,          // `x-left y-top`
            size: str,              // `width height`
        },
    },],
    shape: [TBD],
    table: [TBD],
    text: [{
        content: str,               // `text-content`
        diagram: str,               // `diagram-id`
        id: str,
        style: {
            alignment: str          // `left/center/right`
            colorForeground: number,
            fontSize: number,
            position: str,          // `x-left y-top`
            size: str,              // `width height`
        },
    },],
}
```