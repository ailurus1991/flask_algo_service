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
            console.log(data)
            if(data && data.status === 'OK') {
                $container.html('<img src="' + imgSrc + '" width="' + data.width + '" height="' + data.height + '">');
            } else {
                alert('data error');
                return;
            }

            data.faces && data.faces.map(function (face, i) {
                var $rect = $('<div id="ract_' + i + '"></div>');
                var $attr = $('<ul></ul>');
                var $emot = $('<ul></ul>');
                var propStr = '';

                $rect.css({
                    position: 'absolute',
                    top: face.rect.top,
                    left: face.rect.left,
                    width: face.rect.right - face.rect.left + 'px',
                    height: face.rect.bottom - face.rect.top + 'px',
                    background: 'rgba(0, 0, 0, .3)'
                })

                var ulCss = {
                    color: 'white'
                };
                $attr.css(ulCss)
                $emot.css(ulCss)

                face.attributes && Object.keys(face.attributes).map(function (attrKey, i) {
                    var $li = $('<li></li>');

                    $li.text(attrKey + ' :  ' + face.attributes[attrKey]);

                    $attr.append($li);
                })

                face.emotions && Object.keys(face.emotions).map(function (attrKey, i) {
                    var $li = $('<li></li>');

                    $li.text(attrKey + ' :  ' + face.emotions[attrKey]);

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
    showRect($('.container'), data, './30.pic_hd.jpg');
});