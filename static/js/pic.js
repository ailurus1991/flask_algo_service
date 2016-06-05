// index.js
$(function () {
    /**
     * 根据数据绘制脸部遮罩
     * @param  {[jquery 对象]} $container [图片的容器]
     * @param  {[Object]} data       [绘制的数据对象]
     * @param  {[String]} imgSrc     [图片链接或本地地址]
     * @return {[null]}            [null]
     */
    function showRect($container, data, imgSrc) {
        var img = new Image();

        img.onload = function () {
            // console.log(data)
            // var data = {}
            // data.rect = JSON.parse(data_raw.rect)
            // var data.face_emotions = JSON.parse(data_raw.rect)
            // var data.face_attributes = JSON.parse(data_raw.attributes)
            // var data.rect = JSON.parse(data_raw.rect)
            $container.html('<img src="' + imgSrc + '" width="' + data.width + '" height="' + data.height + '">');

            if (data.verification) {
                var $verification = $('<div></div>');
                var content = 'same_person: ' + data.verification.same_person + ', confidence: ' + data.verification.confidence;
                $verification.text(content);
                $container.append($verification);  
            }

            data.faces && data.faces.map(function (face, i) {
            // var face = data
                var $rect = $('<div id="ract_' + 0 + '"></div>');
                var $attr = $('<ul></ul>');
                var $emot = $('<ul></ul>');
                var propStr = '';

                $rect.css({
                    position: 'absolute',
                    top: face.rect.top,
                    left: face.rect.left,
                    width: face.rect.right - face.rect.left + 'px',
                    height: face.rect.bottom - face.rect.top + 'px',
                    background: 'rgba(0, 0, 0, .3)',
                    whiteSpace: 'nowrap'
                })

                var ulCss = {
                    color: 'white'
                };
                $attr.css(ulCss)
                $emot.css(ulCss)

                face.face_attributes && Object.keys(face.face_attributes).map(function (attrKey, i) {
                    var $li = $('<li></li>');

                    $li.text(attrKey + ' :  ' + face.face_attributes[attrKey]);

                    $attr.append($li);
                })

                face.face_emotions && Object.keys(face.face_emotions).map(function (attrKey, i) {
                    var $li = $('<li></li>');

                    $li.text(attrKey + ' :  ' + face.face_emotions[attrKey]);

                    $emot.append($li);
                })

                $rect.append($attr);
                $rect.append($emot);

                $container.append($rect);
            })

        }
        img.src = imgSrc;
    }

    window.showRect = showRect;
    // showRect($('.container'), data, './30.pic_hd.jpg');
});
