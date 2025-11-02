with open('app.py', 'r') as f:
    lines = f.readlines()

pos = -1
for i, line in enumerate(lines):
    if 'Quick Insights' in line and '##' in line:
        pos = i
        break

if pos == -1:
    print("Error")
else:
    code = '''    if 'engagement_level' in df.columns:
        st.markdown("## 🤖 AI Model Insights")
        c1, c2, c3 = st.columns(3)
        with c1:
            avg = df[['login_count', 'time_spent', 'quiz_attempts']].mean(axis=1).mean()
            st.metric("Avg Engagement", f"{avg:.2f}")
        with c2:
            anom = (df['anomaly'] == -1).mean() * 100
            st.metric("Anomaly Rate", f"{anom:.1f}%")
        with c3:
            st.metric("Clusters", "3 Groups")
        st.markdown("---")
    
'''
    lines.insert(pos, code)
    with open('app.py', 'w') as f:
        f.writelines(lines)
    print("UI Added!")
