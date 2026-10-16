(function hideExpiryWhenMerged() {
    function sync() {
        var merged = document.getElementById('vocabWarningBanner');
        var expiry = document.getElementById('expiryBanner');
        if (!expiry) return;
        
        if (merged && merged.offsetParent !== null) {
            expiry.style.display = 'none';
        } else {
            expiry.style.display = ''; // Khôi phục hiển thị nếu banner cảnh báo biến mất
        }
    }

    // Kiểm tra trạng thái ngay lần đầu tiên
    sync();

    // Sử dụng MutationObserver thay cho setInterval để theo dõi sự thay đổi trên DOM
    var observer = new MutationObserver(function() {
        sync();
    });

    // Lắng nghe thay đổi cấu trúc hoặc thuộc tính trong body để phát hiện banner
    observer.observe(document.body, {
        childList: true,
        subtree: true,
        attributes: true,
        attributeFilter: ['style', 'class', 'hidden']
    });
})();
