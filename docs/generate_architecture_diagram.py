import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch, ArrowStyle

def create_architecture_diagram(output_path):
    fig, ax = plt.subplots(figsize=(19, 14), dpi=150)
    ax.set_xlim(0, 190)
    ax.set_ylim(0, 140)
    ax.axis('off')

    # Color Palette (Official AWS Diagram Palette)
    C_BG = '#FFFFFF'
    C_AWS_BORDER = '#7D8998'
    C_AWS_ORANGE = '#EC7211'
    C_VPC_GREEN = '#248814'
    C_AZ_ORANGE = '#EB5F07'
    C_AZ_BG = '#FCF9F5'
    C_PUB_BG = '#EAF7EB'
    C_PRIV_BG = '#EDF4FA'
    C_PUB_BORDER = '#248814'
    C_PRIV_BORDER = '#0073BB'
    C_PURPLE = '#8C4FFF'
    C_BLUE = '#0073BB'
    C_DARK = '#232F3E'
    C_GRAY = '#545B64'
    C_LIGHT_GRAY = '#EAEDED'
    C_TEXT = '#16191F'
    C_RED = '#D13212'

    # Background
    fig.patch.set_facecolor(C_BG)

    # Helper: draw badge
    def draw_badge(x, y, w, h, bg, text, font_size=10):
        bbox = FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.2,rounding_size=1.0",
                              facecolor=bg, edgecolor=bg, zorder=4)
        ax.add_patch(bbox)
        ax.text(x + w/2, y + h/2, text, color='#FFFFFF', fontsize=font_size,
                fontweight='bold', ha='center', va='center', zorder=5, family='sans-serif')

    # Helper: draw service icon box
    def draw_service_box(cx, cy, label, subtext, icon_color, service_type='compute', width=16, height=13):
        x = cx - width/2
        y = cy - height/2
        # Card background
        card = FancyBboxPatch((x, y), width, height, boxstyle="round,pad=0.2,rounding_size=1.2",
                              facecolor='#FFFFFF', edgecolor='#D5DBDB', linewidth=1.2, zorder=5)
        ax.add_patch(card)
        
        # Icon block
        icon_size = 5.0
        icon_box = FancyBboxPatch((cx - icon_size/2, cy + 1.2), icon_size, icon_size,
                                  boxstyle="round,pad=0.1,rounding_size=0.8",
                                  facecolor=icon_color, edgecolor=icon_color, zorder=6)
        ax.add_patch(icon_box)

        # Service type mark inside icon
        if service_type == 'ec2':
            ax.plot([cx-1.5, cx+1.5, cx+1.5, cx-1.5, cx-1.5], [cy+2.2, cy+2.2, cy+5.2, cy+5.2, cy+2.2], color='#FFFFFF', lw=1.8, zorder=7)
            ax.plot([cx-0.8, cx+0.8], [cy+3.7, cy+3.7], color='#FFFFFF', lw=1.5, zorder=7)
            ax.plot([cx, cx], [cy+2.9, cy+4.5], color='#FFFFFF', lw=1.5, zorder=7)
        elif service_type == 'db':
            # Cylinder / database graphic
            circle = plt.Circle((cx, cy+4.5), 1.4, color='#FFFFFF', fill=False, lw=1.8, zorder=7)
            ax.add_patch(circle)
            ax.plot([cx-1.4, cx-1.4, cx+1.4, cx+1.4], [cy+4.5, cy+2.5, cy+2.5, cy+4.5], color='#FFFFFF', lw=1.8, zorder=7)
        elif service_type == 'nat':
            circle = plt.Circle((cx, cy+3.7), 1.8, color='#FFFFFF', fill=False, lw=1.8, zorder=7)
            ax.add_patch(circle)
            ax.plot([cx-1.2, cx+1.2], [cy+3.7, cy+3.7], color='#FFFFFF', lw=1.8, zorder=7)
            ax.plot([cx, cx], [cy+2.5, cy+4.9], color='#FFFFFF', lw=1.8, zorder=7)
        elif service_type == 's3':
            # Bucket graphic
            ax.plot([cx-1.6, cx+1.6, cx+1.2, cx-1.2, cx-1.6], [cy+5.0, cy+5.0, cy+2.4, cy+2.4, cy+5.0], color='#FFFFFF', lw=1.8, zorder=7)
        elif service_type == 'shield':
            # Shield / WAF
            ax.plot([cx-1.5, cx+1.5, cx+1.2, cx, cx-1.2, cx-1.5], [cy+5.2, cy+5.2, cy+3.4, cy+2.2, cy+3.4, cy+5.2], color='#FFFFFF', lw=1.8, zorder=7)
        elif service_type == 'dns':
            # 53 / DNS
            ax.text(cx, cy+3.7, '53', color='#FFFFFF', fontsize=11, fontweight='bold', ha='center', va='center', zorder=7)
        elif service_type == 'cdn':
            circle1 = plt.Circle((cx, cy+3.7), 1.8, color='#FFFFFF', fill=False, lw=1.8, zorder=7)
            circle2 = plt.Circle((cx, cy+3.7), 0.7, color='#FFFFFF', fill=True, zorder=7)
            ax.add_patch(circle1)
            ax.add_patch(circle2)
        elif service_type == 'ssm':
            # Terminal / SSM
            ax.plot([cx-1.6, cx+1.6, cx+1.6, cx-1.6, cx-1.6], [cy+2.4, cy+2.4, cy+5.0, cy+5.0, cy+2.4], color='#FFFFFF', lw=1.8, zorder=7)
            ax.text(cx, cy+3.7, '>', color='#FFFFFF', fontsize=9, fontweight='bold', ha='center', va='center', zorder=7)
        elif service_type == 'lightsail':
            ax.text(cx, cy+3.7, 'LS', color='#FFFFFF', fontsize=10, fontweight='bold', ha='center', va='center', zorder=7)

        # Label & subtext
        ax.text(cx, cy - 2.5, label, color=C_TEXT, fontsize=9.5, fontweight='bold', ha='center', va='center', zorder=7, family='sans-serif')
        ax.text(cx, cy - 4.5, subtext, color=C_GRAY, fontsize=8.0, ha='center', va='center', zorder=7, family='sans-serif')

    # ==================== 1. OUTER AWS CLOUD BOUNDARY ====================
    aws_box = FancyBboxPatch((5, 5), 180, 130, boxstyle="round,pad=0.5,rounding_size=2.0",
                             facecolor='#FFFFFF', edgecolor=C_AWS_BORDER, linewidth=1.8, zorder=1)
    ax.add_patch(aws_box)
    draw_badge(5, 131, 22, 4.5, C_AWS_ORANGE, 'AWS Cloud', font_size=11)

    # Title Banner at Top
    ax.text(95, 132.5, 'AWS Capstone Projects: Enterprise Multi-Tier & Edge Architecture',
            color=C_DARK, fontsize=15, fontweight='bold', ha='center', va='center', zorder=5, family='sans-serif')

    # ==================== 2. TOP EDGE LAYER: USERS, DNS, CDN & WAF ====================
    # External Users Box (Left Top)
    user_box = FancyBboxPatch((10, 107), 38, 16, boxstyle="round,pad=0.3,rounding_size=1.5",
                              facecolor='#F8F9FA', edgecolor='#CCD1D9', linewidth=1.2, zorder=3)
    ax.add_patch(user_box)
    ax.text(29, 120, 'Global Web Traffic', color=C_DARK, fontsize=10, fontweight='bold', ha='center', va='center', zorder=5)
    ax.text(29, 115.5, 'Africa, Asia, Global (Allowed)', color=C_VPC_GREEN, fontsize=8.5, fontweight='bold', ha='center', va='center', zorder=5)
    ax.text(29, 111, 'Russia / Blocked Regions (Restricted)', color=C_RED, fontsize=8.5, fontweight='bold', ha='center', va='center', zorder=5)

    # Route 53
    draw_service_box(68, 115, 'Amazon Route 53', 'DNS & Failover Routing', C_PURPLE, service_type='dns')

    # CloudFront
    draw_service_box(102, 115, 'Amazon CloudFront', 'Global CDN Edge Cache', C_PURPLE, service_type='cdn')

    # AWS WAF & Geo Restrictions
    draw_service_box(136, 115, 'AWS WAF / Geo-Match', 'AF/AS Allow | RU Block', C_AWS_ORANGE, service_type='shield')

    # Connection: Users -> Route 53 -> CloudFront -> WAF
    ax.annotate('', xy=(59, 115), xytext=(48, 115),
                arrowprops=dict(arrowstyle="-|>", color=C_DARK, lw=2.0, mutation_scale=14), zorder=8)
    ax.annotate('', xy=(93, 115), xytext=(77, 115),
                arrowprops=dict(arrowstyle="-|>", color=C_DARK, lw=2.0, mutation_scale=14), zorder=8)
    ax.annotate('', xy=(127, 115), xytext=(111, 115),
                arrowprops=dict(arrowstyle="<|-|>", color=C_AWS_ORANGE, lw=2.0, mutation_scale=14), zorder=8)

    # ==================== 3. PRODUCTION VPC BOUNDARY ====================
    vpc_box = FancyBboxPatch((10, 12), 132, 85, boxstyle="round,pad=0.5,rounding_size=2.0",
                             facecolor='#FFFFFF', edgecolor=C_VPC_GREEN, linewidth=2.2, zorder=2)
    ax.add_patch(vpc_box)
    draw_badge(10, 93, 12, 4.2, C_VPC_GREEN, 'VPC', font_size=10)
    ax.text(26, 95, 'Production VPC (10.0.0.0/16)', color=C_VPC_GREEN, fontsize=11, fontweight='bold', va='center', zorder=5)

    # Internet Gateway (Top of VPC)
    draw_service_box(45, 87, 'Internet Gateway', '0.0.0.0/0 Direct Ingress', C_PURPLE, service_type='nat', width=18, height=10)

    # Public Route Table
    draw_service_box(80, 87, 'Public Route Table', 'Routes to IGW (0.0.0.0/0)', C_PURPLE, service_type='nat', width=18, height=10)

    # Arrow from CloudFront down to IGW
    ax.annotate('', xy=(45, 93), xytext=(102, 107),
                arrowprops=dict(arrowstyle="-|>", color=C_DARK, lw=2.0, mutation_scale=14), zorder=8)
    # Arrow IGW <-> Public Route Table
    ax.annotate('', xy=(70, 87), xytext=(55, 87),
                arrowprops=dict(arrowstyle="<|-|>", color=C_PURPLE, lw=1.8, mutation_scale=12), zorder=8)

    # ==================== 4. AVAILABILITY ZONE 1A & 1B ====================
    # AZ 1A Container
    az_box = FancyBboxPatch((14, 16), 124, 64, boxstyle="round,pad=0.4,rounding_size=1.5",
                            facecolor=C_AZ_BG, edgecolor=C_AZ_ORANGE, linewidth=1.6, linestyle='--', zorder=3)
    ax.add_patch(az_box)
    draw_badge(14, 76, 26, 4.0, C_AZ_ORANGE, 'Availability Zone 1A', font_size=9.5)

    # --- Public Subnet (Green) ---
    pub_sub = FancyBboxPatch((18, 20), 55, 52, boxstyle="round,pad=0.4,rounding_size=1.2",
                             facecolor=C_PUB_BG, edgecolor=C_PUB_BORDER, linewidth=1.5, zorder=4)
    ax.add_patch(pub_sub)
    draw_badge(18, 68, 30, 3.8, C_PUB_BORDER, 'Public Subnet (10.0.1.0/24)', font_size=8.5)

    # Frontend Web Server in Public Subnet
    draw_service_box(45, 54, 'Frontend Web Server', 'EC2 t2.micro | Apache\nPublic IP: Assigned', C_AWS_ORANGE, service_type='ec2', width=22, height=14)

    # NAT Gateway in Public Subnet
    draw_service_box(45, 31, 'AWS NAT Gateway', 'Elastic IP Attached\nOutbound Translation', C_PURPLE, service_type='nat', width=22, height=13)

    # --- Private Subnet (Blue) ---
    priv_sub = FancyBboxPatch((79, 20), 55, 52, boxstyle="round,pad=0.4,rounding_size=1.2",
                              facecolor=C_PRIV_BG, edgecolor=C_PRIV_BORDER, linewidth=1.5, zorder=4)
    ax.add_patch(priv_sub)
    draw_badge(79, 68, 30, 3.8, C_PRIV_BORDER, 'Private Subnet (10.0.2.0/24)', font_size=8.5)

    # Backend Database in Private Subnet
    draw_service_box(106, 54, 'Backend Database', 'EC2 MariaDB 10.5\nPrivate IP Only (No Public)', C_BLUE, service_type='db', width=22, height=14)

    # Private Route Table inside Private Subnet
    draw_service_box(106, 31, 'Private Route Table', '0.0.0.0/0 -> NAT Gateway\nIsolated Inbound', C_PURPLE, service_type='nat', width=22, height=13)

    # Inter-subnet Arrows & Flows
    # IGW to Frontend Web Server
    ax.annotate('', xy=(45, 62), xytext=(45, 81),
                arrowprops=dict(arrowstyle="-|>", color=C_DARK, lw=2.0, mutation_scale=14), zorder=8)
    
    # Frontend Web Server to Backend DB (Port 3306)
    ax.annotate('', xy=(94, 54), xytext=(57, 54),
                arrowprops=dict(arrowstyle="-|>", color=C_DARK, lw=2.0, mutation_scale=14), zorder=8)
    bbox_port = FancyBboxPatch((69, 52), 13, 4.5, boxstyle="round,pad=0.1,rounding_size=0.6",
                               facecolor='#FFFFFF', edgecolor='#7D8998', linewidth=1.0, zorder=9)
    ax.add_patch(bbox_port)
    ax.text(75.5, 54.2, 'Port 3306', color=C_DARK, fontsize=8, fontweight='bold', ha='center', va='center', zorder=10)

    # Requirement 1: Database outbound updates via NAT Gateway
    ax.annotate('', xy=(57, 31), xytext=(94, 31),
                arrowprops=dict(arrowstyle="-|>", color=C_BLUE, lw=2.0, linestyle='--', mutation_scale=14), zorder=8)
    bbox_req1 = FancyBboxPatch((66, 33), 19, 4.2, boxstyle="round,pad=0.1,rounding_size=0.6",
                               facecolor='#E8F4FD', edgecolor=C_BLUE, linewidth=1.0, zorder=9)
    ax.add_patch(bbox_req1)
    ax.text(75.5, 35.1, 'Req 1: Outbound Updates', color=C_BLUE, fontsize=7.5, fontweight='bold', ha='center', va='center', zorder=10)

    # NAT Gateway to IGW for internet outbound
    ax.annotate('', xy=(34, 84), xytext=(34, 38),
                arrowprops=dict(arrowstyle="-|>", color=C_BLUE, lw=1.8, linestyle=':', mutation_scale=12), zorder=8)

    # ==================== 5. COMPLIANCE & EXTERNAL STORAGE SERVICES ====================
    # Requirement 2: AWS Systems Manager (SSM) Session Manager (Right Column)
    ssm_box = FancyBboxPatch((148, 55), 33, 42, boxstyle="round,pad=0.4,rounding_size=1.5",
                             facecolor='#FAF5FF', edgecolor=C_PURPLE, linewidth=1.5, zorder=3)
    ax.add_patch(ssm_box)
    draw_badge(148, 93, 26, 3.8, C_PURPLE, 'AWS Systems Manager', font_size=8.5)

    draw_service_box(164.5, 78, 'SSM Session Manager', 'Remote Admin Access\nZero Inbound Ports (No SSH)', C_PURPLE, service_type='ssm', width=26, height=13)

    # Requirement 2 explanation badge
    ax.text(164.5, 66, 'Requirement 2 Solution:', color=C_PURPLE, fontsize=8.5, fontweight='bold', ha='center', va='center', zorder=5)
    ax.text(164.5, 62, 'Encrypted TLS 443 Admin Shell\nNo Public IP / Port 22 Closed', color=C_GRAY, fontsize=7.5, ha='center', va='center', zorder=5)

    # Arrow from Developer/SSM into DB
    ax.annotate('', xy=(118, 54), xytext=(151, 74),
                arrowprops=dict(arrowstyle="-|>", color=C_PURPLE, lw=2.0, mutation_scale=14), zorder=8)

    # Amazon S3 Bucket (Project 3)
    s3_box = FancyBboxPatch((148, 12), 33, 38, boxstyle="round,pad=0.4,rounding_size=1.5",
                            facecolor='#F4FBF5', edgecolor=C_VPC_GREEN, linewidth=1.5, zorder=3)
    ax.add_patch(s3_box)
    draw_badge(148, 46, 22, 3.8, C_VPC_GREEN, 'Storage & Hosting', font_size=8.5)

    draw_service_box(164.5, 33, 'Amazon S3 Origin', 'Static Website Hosting\nBlock Public Access: ON', C_VPC_GREEN, service_type='s3', width=26, height=13)
    draw_service_box(164.5, 19, 'Amazon Lightsail', 'Low-Cost WordPress Store\nFlat $3.50/mo + Free SSL', C_AWS_ORANGE, service_type='lightsail', width=26, height=11)

    # Arrow from CloudFront to S3 (Origin Access Control OAC)
    ax.annotate('', xy=(164.5, 41), xytext=(111, 107),
                arrowprops=dict(arrowstyle="-|>", color=C_VPC_GREEN, lw=2.0, linestyle='--', mutation_scale=14), zorder=8)
    bbox_oac = FancyBboxPatch((125, 96), 25, 4.0, boxstyle="round,pad=0.1,rounding_size=0.6",
                              facecolor='#EAF7EB', edgecolor=C_VPC_GREEN, linewidth=1.0, zorder=9)
    ax.add_patch(bbox_oac)
    ax.text(137.5, 98, 'Origin Access Control (OAC)', color=C_VPC_GREEN, fontsize=7.5, fontweight='bold', ha='center', va='center', zorder=10)

    # Footer Notes Box
    footer_box = FancyBboxPatch((10, 6), 170, 4.5, boxstyle="round,pad=0.1,rounding_size=0.6",
                                facecolor='#F8F9FA', edgecolor='#D5DBDB', linewidth=0.8, zorder=3)
    ax.add_patch(footer_box)
    ax.text(95, 8.2, 'Author: Purity Njeri Ngugi | AWS re/Start Capstone Portfolio | Validated on AWS Cloud Services',
            color=C_GRAY, fontsize=8.5, ha='center', va='center', zorder=5)

    plt.tight_layout()
    plt.savefig(output_path, dpi=180, facecolor=C_BG, bbox_inches='tight')
    plt.close()
    print(f"Generated architecture diagram successfully: {output_path}")

if __name__ == '__main__':
    create_architecture_diagram('c:/Users/PURITY/Downloads/conference-website/docs/images/capstone-portfolio-architecture.png')
