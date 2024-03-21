from PIL import Image, ImageFont, ImageDraw

class NewsPostTemplate(object):
    MARGINS_SIZE = 30
    SPACE_SIZE = 20
    TITLE_SIZE = 48
    WARNING_TEXT_SIZE = 24
    CONTACT_TEXT_SIZE = 36
    CONTACT_QRCODE_SIZE = 300

    def __init__(
        self,
        info_image: bytes,
        title: str = "吕梁生活",
        waring_text: str = "禁止发广告",
        qr_code: str = "src/resource/mm_qrcode.jpg",
    ) -> None:
        self.info_image = Image.open(info_image)
        self.title = title
        self.waring_text = waring_text
        self.qr_code = qr_code
        self.poster_width, self.poster_height = self.calculate_poster_size()
        background_color = (255, 255, 255)
        self.poster = Image.new(
            "RGB", (self.poster_width, self.poster_height), background_color
        )
        self.draw = ImageDraw.Draw(self.poster)
        self.current_position_y = 0
        self.draw_poster()

    def calculate_poster_size(self) -> tuple:
        width, height = self.info_image.size
        if width > 800:
            width_percent = 800 / width
            height = int(height * width_percent)
            self.info_image = self.info_image.resize((800, height))
            width, height = self.info_image.size
        poster_width = width + 2 * self.MARGINS_SIZE
        poster_height = (
            height
            + 2 * self.MARGINS_SIZE
            + 3 * self.SPACE_SIZE
            + self.CONTACT_QRCODE_SIZE
            + self.TITLE_SIZE
            + self.WARNING_TEXT_SIZE
        )
        return (poster_width, poster_height)

    def draw_title(self) -> None:
        self.current_position_y += self.MARGINS_SIZE
        title_font = ImageFont.truetype(
            "src/resource/font/Xiaolai.ttf", self.TITLE_SIZE
        )
        title_position_x = (self.poster_width - len(self.title) * self.TITLE_SIZE) // 2
        title_color = (0, 0, 0)
        self.draw.text(
            (title_position_x, self.current_position_y),
            self.title,
            font=title_font,
            fill=title_color,
        )

    def paste_info_image(self) -> None:
        self.current_position_y = self.current_position_y + self.TITLE_SIZE + self.SPACE_SIZE
        self.poster.paste(self.info_image, (self.MARGINS_SIZE, self.current_position_y))

    def draw_warning_text(self) -> None:
        self.current_position_y = self.info_image.size[1] + self.current_position_y + self.SPACE_SIZE
        warning_font = ImageFont.truetype(
            "src/resource/font/Xiaolai.ttf", self.WARNING_TEXT_SIZE
        )
        warning_text_color = (0, 0, 0)
        for i in range(2):
            sub_x = (
                self.poster_width - self.WARNING_TEXT_SIZE * len(self.waring_text) * 2
            ) // 2 // 2 + i * (
                self.poster_width - self.WARNING_TEXT_SIZE * len(self.waring_text)
            ) // 2
            self.draw.text(
                (sub_x, self.current_position_y),
                text=self.waring_text,
                font=warning_font,
                fill=warning_text_color,
            )

    def draw_contact_qrcode(self) -> None:
        self.current_position_y = (
            self.current_position_y + self.WARNING_TEXT_SIZE + self.SPACE_SIZE
        )
        qr_code = Image.open(self.qr_code)
        qr_code = qr_code.resize((self.CONTACT_QRCODE_SIZE, self.CONTACT_QRCODE_SIZE))
        qr_code_position_x = (
            self.poster_width // 2
            + (self.poster_width // 2 - self.CONTACT_QRCODE_SIZE) // 2
        )
        self.poster.paste(qr_code, (qr_code_position_x, self.current_position_y))

    def draw_contact_text(self) -> None:
        self.current_position_y = (
            self.current_position_y
            + (self.CONTACT_QRCODE_SIZE // 2 - self.CONTACT_TEXT_SIZE) // 2
        )
        contact_text = ["更多信息请扫码加微信", "发送“生活”进群"]
        contact_font = ImageFont.truetype(
            "src/resource/font/Xiaolai.ttf", self.CONTACT_TEXT_SIZE
        )
        t_color = (0, 0, 0)
        for t in contact_text:
            t_position_x = (
                self.poster_width // 2 - len(t) * self.CONTACT_TEXT_SIZE
            ) // 2
            self.draw.text(
                (t_position_x+self.SPACE_SIZE, self.current_position_y),
                t,
                font=contact_font,
                fill=t_color,
            )
            self.current_position_y = (
                self.current_position_y
                + (self.CONTACT_QRCODE_SIZE - 2 * self.CONTACT_TEXT_SIZE) // 2
            )

    def draw_poster(self) -> None:
        self.draw_title()
        self.paste_info_image()
        self.draw_warning_text()
        self.draw_contact_qrcode()
        self.draw_contact_text()

    def save(self, filename) -> None:
        self.poster.save(filename)
