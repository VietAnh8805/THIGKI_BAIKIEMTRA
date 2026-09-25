from flask import Flask, render_template_string, request


app = Flask(__name__)

TRANG_HTML = """
<!doctype html>
<html lang="vi">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Biểu đồ sinh viên</title>
    <style>
        :root { color-scheme: light; font-family: Georgia, "Times New Roman", serif; background: #f3efe7; color: #253238; }
        * { box-sizing: border-box; }
        body { margin: 0; min-height: 100vh; padding: 40px 20px; }
        main { max-width: 920px; margin: auto; }
        header { margin-bottom: 28px; }
        h1 { font-size: clamp(2rem, 6vw, 4.5rem); line-height: .95; margin: 0 0 12px; }
        p { font-family: Arial, sans-serif; color: #5e6b70; }
        .layout { display: grid; grid-template-columns: 280px 1fr; gap: 24px; align-items: stretch; }
        .panel, .chart { background: #fffdf8; border: 1px solid #d9d0c1; border-radius: 8px; padding: 24px; }
        label { display: block; font: 600 14px Arial, sans-serif; margin: 16px 0 7px; }
        input { width: 100%; border: 1px solid #b9b1a5; border-radius: 4px; padding: 12px; font: 18px Arial, sans-serif; }
        button { width: 100%; margin-top: 22px; border: 0; border-radius: 4px; padding: 13px; background: #db6b45; color: white; font: 700 15px Arial, sans-serif; cursor: pointer; }
        button:hover { background: #bd5132; }
        .error { padding: 10px; border-left: 4px solid #b83434; background: #fbe9e5; color: #8f2525; font: 14px Arial, sans-serif; }
        .chart { min-height: 390px; display: flex; flex-direction: column; }
        .chart h2 { margin: 0 0 24px; font-size: 22px; }
        .bars { flex: 1; min-height: 260px; display: flex; align-items: end; justify-content: center; gap: clamp(35px, 12vw, 100px); border-bottom: 1px solid #b9b1a5; padding: 0 20px; }
        .bar-group { width: 90px; height: 100%; display: flex; flex-direction: column; justify-content: end; align-items: center; gap: 9px; }
        .bar { width: 72px; min-height: 3px; border-radius: 5px 5px 0 0; transition: height .3s ease; }
        .bar.male { background: #376f8f; }
        .bar.female { background: #d97568; }
        .value { font: 700 20px Arial, sans-serif; }
        .name { font: 600 14px Arial, sans-serif; margin-bottom: -27px; transform: translateY(30px); }
        .summary { margin: 26px 0 0; font: 14px Arial, sans-serif; color: #5e6b70; }
        @media (max-width: 650px) { body { padding: 24px 14px; } .layout { grid-template-columns: 1fr; } .chart { min-height: 350px; } }
    </style>
</head>
<body>
<main>
    <header>
        <p>THỐNG KÊ LỚP HỌC</p>
        <h1>Nam và nữ trong lớp</h1>
        <p>Nhập số lượng để xem biểu đồ cột.</p>
    </header>
    <section class="layout">
        <form class="panel" method="post">
            <label for="so_nam">Sinh viên nam</label>
            <input id="so_nam" name="so_nam" type="number" min="0" required value="{{ so_nam }}">
            <label for="so_nu">Sinh viên nữ</label>
            <input id="so_nu" name="so_nu" type="number" min="0" required value="{{ so_nu }}">
            {% if loi %}<p class="error">{{ loi }}</p>{% endif %}
            <button type="submit">Cập nhật biểu đồ</button>
        </form>
        <section class="chart">
            <h2>Số lượng sinh viên</h2>
            <div class="bars">
                <div class="bar-group">
                    <span class="value">{{ so_nam }}</span>
                    <div class="bar male" style="height: {{ chieu_cao_nam }}%"></div>
                    <span class="name">Nam</span>
                </div>
                <div class="bar-group">
                    <span class="value">{{ so_nu }}</span>
                    <div class="bar female" style="height: {{ chieu_cao_nu }}%"></div>
                    <span class="name">Nữ</span>
                </div>
            </div>
            <p class="summary">Tổng số sinh viên: <strong>{{ tong_so }}</strong></p>
        </section>
    </section>
</main>
</body>
</html>
"""


@app.route("/", methods=["GET", "POST"])
def trang_chu():
    so_nam = 0
    so_nu = 0
    loi = ""

    if request.method == "POST":
        try:
            so_nam = int(request.form.get("so_nam", ""))
            so_nu = int(request.form.get("so_nu", ""))
            if so_nam < 0 or so_nu < 0:
                raise ValueError
        except ValueError:
            so_nam = 0
            so_nu = 0
            loi = "Vui lòng nhập hai số nguyên không âm."

    tong_so = so_nam + so_nu
    muc_lon_nhat = max(so_nam, so_nu, 1)
    chieu_cao_nam = max(so_nam / muc_lon_nhat * 85, 1)
    chieu_cao_nu = max(so_nu / muc_lon_nhat * 85, 1)

    return render_template_string(
        TRANG_HTML,
        so_nam=so_nam,
        so_nu=so_nu,
        tong_so=tong_so,
        chieu_cao_nam=chieu_cao_nam,
        chieu_cao_nu=chieu_cao_nu,
        loi=loi,
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=1576, debug=True)
