# Project 4: Low-Cost WordPress E-Commerce Website with Custom Domain on AWS

## Project Overview
An e-commerce startup requires an online store with three primary constraints:
1. **Simple Management Interface:** Easy-to-manage CMS dashboard for inventory and orders.
2. **Minimal Development & Operating Cost:** Flat, predictable monthly pricing with zero licensing overhead.
3. **Custom DNS Name:** Associated domain name (e.g., `store.yourdomain.com`).

---

## Architectural Comparison

| Parameter | Amazon Lightsail (Recommended) | Multi-Tier EC2 + RDS |
| :--- | :--- | :--- |
| **Setup Overhead** | 1-Click pre-configured Bitnami blueprint | Manual VPC, subnets, EC2, RDS, and LAMP setup |
| **Console Experience** | Simplified developer/startup dashboard | Enterprise AWS management console |
| **Cost Predictability** | Flat bundle from $3.50/month (Compute + Storage + Transfer) | Variable compute, I/O charges, NAT gateway fees |
| **SSL Setup** | Integrated `bncert-tool` for automated Let's Encrypt | Manual Certbot / ALB ACM configuration |

*Conclusion:* **Amazon Lightsail** fulfills the startup requirements for minimal cost and simplified management.

---

## Architecture Diagram

```
[Store Customers] ---------> Custom DNS (Route 53 / A-Record) ---------> Lightsail Static IP
                                                                                 |
                                                                           (Port 80/443)
                                                                                 v
                                                                     Lightsail WordPress Instance
                                                                     ├── Bitnami WordPress Core
                                                                     ├── Apache + PHP 8.x
                                                                     ├── Local MariaDB
                                                                     └── Let's Encrypt SSL
```

---

## Step-by-Step Implementation Guide

### Step 1: Launch Amazon Lightsail Instance
1. Open the **Amazon Lightsail** console (`https://lightsail.aws.amazon.com/`).
2. Click **Create instance**:
   * **Platform:** Linux/Unix
   * **Blueprint:** Apps + OS -> **WordPress**
   * **Instance plan:** $3.50/month tier
   * **Instance name:** `ecommerce-startup-wp`
3. Click **Create instance**.

---

### Step 2: Attach a Static IP
1. In the Lightsail console, navigate to the **Networking** tab.
2. Click **Create static IP**.
3. Attach the static IP to `ecommerce-startup-wp`.
4. Name the resource: `wp-static-ip` and save.

---

### Step 3: Configure Custom DNS Domain
1. In Route 53 or your external domain registrar:
2. Add an **A Record**:
   * Name: `store` (or `@` for apex domain)
   * Value: Enter your **Lightsail Static IP**
   * TTL: 300 seconds

---

### Step 4: Configure Free SSL/TLS (Let's Encrypt)
1. In the Lightsail console, click the terminal icon on your instance card to open SSH.
2. Run the Bitnami SSL configuration tool:
   ```bash
   sudo /opt/bitnami/bncert-tool
   ```
3. Enter your domain name and enable HTTP to HTTPS redirection.
4. Complete the prompts to generate and install the certificate.

---

### Step 5: Admin Login and Store Configuration
1. Retrieve the default administrator credentials from the terminal:
   ```bash
   cat bitnami_application_password
   ```
2. In your browser, open `https://<your-domain>/wp-admin`.
3. Log in with username `user` and the retrieved password.
4. Navigate to **Plugins** -> **Add New** -> Install and activate **WooCommerce**.

---

## Alternative: EC2 Free Tier Scripted Setup
To run on standard EC2 Free Tier rather than Lightsail:
1. Launch an Amazon Linux 2023 `t2.micro` instance.
2. Connect and run:
   ```bash
   chmod +x setup-wordpress-ec2.sh
   sudo ./setup-wordpress-ec2.sh
   ```
3. Open `http://<EC2-PUBLIC-IP>` to complete setup.

---

## Demonstration & Verification
1. **DNS Resolution:** Run `nslookup store.yourdomain.com` to verify resolution to the Static IP.
2. **Secure HTTPS:** Open `https://store.yourdomain.com` to verify valid SSL certificate padlock.
3. **Store Management:** Log in to the `/wp-admin` dashboard and review the WooCommerce product catalog.
4. *Screenshot Evidence:* Capture the secure HTTPS homepage and the WooCommerce product management screen.

---

## Clean-up Instructions
1. In Lightsail, select instance `ecommerce-startup-wp` -> **Delete**.
2. In the **Networking** tab, delete the static IP `wp-static-ip`.
