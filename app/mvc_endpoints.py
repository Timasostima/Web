from flask import Blueprint, render_template, redirect, url_for

from app import bcrypt
from app.forms import LoginForm, RegisterForm
from app.models import db, User
from app.data_classes import Service, News
from flask_login import login_user, login_required, logout_user, current_user


mvc_bp = Blueprint('mvc', __name__)


@mvc_bp.route('/')
def index():
    # if not current_user.is_authenticated:
    #     return redirect(url_for('mvc.login'))
    return render_template("index.html")


@mvc_bp.route('/services')
def services():
    services_list = [
        Service("Sea freight", "Sea freight is one of the basic services provided by Formag."),
        Service("Air transportation", "Air transportation is the fastest and the most reliable way of delivery."),
        Service("Tracking",
                "The Formag company has own modern car park, long-term contracts with transport companies."),
        Service("Railway transportation",
                "Railway delivery is economical and fast. Formag carries out both delivery in Ukraine and cargo transportation from Asia."),
        Service("Warehouse complex",
                "Formag Forwarding transhipment and storage complex is modern equipment and a team of the best specialists in the industry."),
        Service("Insurance and custom clearance",
                "Formag is an agent of Megapolis Insurance Partnership, which occupies a leading position in the field of cargo insurance."),
        Service("LTL deliveries",
                "LTL transportation advantages are obvious: if you need to deliver a small consignment, it will be much more profitable to use consolidated truck and to share transportation charges with other shippers."),
        Service("Port forwarding",
                "While performing the freight forwarding we constantly notify customers on the matter of their cargos’ status and cooperate with port authorities and customs directly to provide the service of the highest quality."),
    ]
    return render_template('Services.html', services=services_list)


@mvc_bp.route('/news')
def news():
    news_items = [
        News("article1.jpg", "Oceanic Oddity", "01.01.2022",
             "Mysterious containers wash ashore on a small island, locals find them filled with antique pirate treasures and rare artifacts.",
             "Article1.html",
             "In a turn of events straight out of a maritime legend, the tranquil island of Isla del Tesoro became the center of the world’s curiosity as several antique containers emerged on its shores. The containers, believed to be remnants of a shipwreck, were filled with a treasure trove of pirate relics. Gold coins, jewelry encrusted with precious stones, and rare artifacts were among the items found, sparking theories of their origin. Historians suggest these could belong to the infamous pirate Blackbeard, whose ship was lost in a storm in the 1700s. The discovery has not only attracted treasure hunters but also historians and archaeologists eager to delve into the contents that could rewrite maritime history. The local government is considering establishing a museum to house these treasures, turning the island into a hub for pirate history enthusiasts."),
        News("article2.jpg", "Skyward Surprise", "01.01.2022",
             "Air shipment accidentally drops thousands of rubber ducks in town square, creating an impromptu festival for delighted residents.",
             "Article2.html",
             "An unexpected event occurred when an air shipment accidentally dropped thousands of rubber ducks in the town square. The incident turned into an impromptu festival, delighting residents and creating a unique spectacle. The rubber ducks, originally intended for a promotional event, became a source of joy and entertainment for the community. The town square was filled with laughter and excitement as people of all ages gathered to witness the unusual sight. The event has since become a cherished memory for the residents, highlighting the unexpected joys that can arise from everyday occurrences."),
        News("article3.jpg", "Glacial Gift", "01.01.2022",
             "Arctic shipment lost for decades found intact, revealing perfectly preserved exotic fruits once thought extinct.",
             "Article3.html",
             "A remarkable discovery was made when an Arctic shipment lost for decades was found intact. The shipment contained perfectly preserved exotic fruits that were once thought to be extinct. The discovery has sparked interest among botanists and historians, as the fruits provide a glimpse into the agricultural practices of the past. The preserved fruits have been carefully studied and analyzed, revealing valuable information about their origins and cultivation methods. The find has also generated excitement among food enthusiasts, who are eager to taste these rare and ancient fruits. The discovery serves as a reminder of the enduring mysteries of the natural world and the potential for uncovering hidden treasures."),
        News("article4.jpg", "Midnight Carousel", "01.01.2022",
             "Nighttime shipment of carousel horses causes whimsical traffic jam, enchanting commuters with a magical roadside merry-go-round.",
             "Article4.html",
             "A whimsical traffic jam occurred when a nighttime shipment of carousel horses caused a magical roadside merry-go-round. The enchanting sight captivated commuters, who were delighted by the unexpected spectacle. The carousel horses, beautifully crafted and adorned with intricate details, created a sense of wonder and nostalgia. The event brought a touch of magic to the otherwise mundane commute, leaving a lasting impression on those who witnessed it. The incident has since become a beloved story in the community, symbolizing the joy and enchantment that can be found in everyday moments."),
        News("article5.jpg", "Desert Delivery", "01.01.2022",
             "Sandstorm uncovers ancient shipment of spices, reviving lost recipes and flavors in a remote desert village.",
             "Article5.html",
             "A sandstorm in a remote desert village uncovered an ancient shipment of spices, reviving lost recipes and flavors. The discovery has brought new life to the village, as the spices have been used to recreate traditional dishes that had long been forgotten. The villagers have embraced the opportunity to reconnect with their culinary heritage, sharing the revived recipes with visitors and neighboring communities. The spices have also attracted the attention of chefs and food enthusiasts, who are eager to experiment with the unique flavors. The event has revitalized the village, turning it into a destination for those seeking to experience the rich and diverse culinary traditions of the region.")
    ]
    return render_template('News.html', news_items=news_items)


@mvc_bp.route('/career')
def career():
    return render_template("Career.html")


@mvc_bp.route('/about-us')
def about_us():
    return render_template("About-us.html")


@mvc_bp.route('/contact')
def contact():
    return render_template("Contact.html")


@mvc_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            print("herw")
            login_user(user)
            return redirect(url_for('mvc.dashboard'))
    return render_template("Login.html", form=form)


@mvc_bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data)
        user = User(username=form.username.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('mvc.login'))
    return render_template("Register.html", form=form)


@mvc_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('mvc.index'))


@mvc_bp.route('/dashboard')
@login_required
def dashboard():
    print("here")
    return render_template('dashboard.html')