#!/bin/bash
dnf update -y
dnf install -y httpd

systemctl start httpd
systemctl enable httpd

cat << 'EOF' > /var/www/html/index.html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>AfriAsia Mart</title>
  <style>
    * { box-sizing: border-box; margin: 0; padding: 0; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Arial, sans-serif; }
    body { background: #f8fafc; color: #1e293b; padding: 2rem; }
    .card { max-width: 600px; margin: 2rem auto; background: white; padding: 2rem; border-radius: 8px; border: 1px solid #e2e8f0; }
    h1 { font-size: 1.5rem; margin-bottom: 0.5rem; color: #0f172a; }
    p { color: #64748b; margin-bottom: 1rem; }
    .tag { display: inline-block; padding: 0.25rem 0.6rem; background: #f0fdfa; color: #0f766e; border-radius: 4px; font-size: 0.85rem; font-weight: 600; }
  </style>
</head>
<body>
  <div class="card">
    <span class="tag">Geo-Restricted</span>
    <h1 style="margin-top: 1rem;">AfriAsia Mart Online</h1>
    <p>Origin server active on Amazon EC2. Distribution protected by CloudFront & AWS WAF.</p>
  </div>
</body>
</html>
EOF

chmod 644 /var/www/html/index.html
