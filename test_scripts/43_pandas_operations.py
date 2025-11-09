def pandas_operations():
    import pandas as pd
    
    # Create DataFrame
    df = pd.DataFrame({
        'A': range(5000),
        'B': [i**2 for i in range(5000)],
        'C': [i*2 for i in range(5000)]
    })
    
    # Operations
    df['D'] = df['A'] + df['B']
    df['E'] = df['C'] * 2
    
    # Groupby
    df['Group'] = df['A'] % 10
    grouped = df.groupby('Group').sum()
    
    return len(grouped)

pandas_operations()