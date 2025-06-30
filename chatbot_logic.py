import time
import yfinance as yf
from difflib import get_close_matches

# 📚 Predefined FAQs
import random
finance_faq = {
    "what is a stock": [
        "A stock is a unit of ownership in a company, giving the investor a share in the company’s profits and assets.",
        "A stock represents a small piece of a company that an investor can buy to gain partial ownership and potential returns.",
        "A stock is an equity instrument that allows someone to invest in a company’s future by purchasing a portion of its value.",
        "A stock is a financial asset that gives the holder a claim on part of a business’s performance and earnings.",
        "A stock offers an opportunity to participate in a company’s growth through appreciation in value and dividend income."
    ],
    "what are mutual funds": [
        "A mutual fund is a professionally managed investment fund that pools money from many investors to buy a diversified mix of securities.",
        "A mutual fund collects money from multiple people and invests it across stocks, bonds, or other assets for long-term growth.",
        "A mutual fund is an investment product that spreads risk by investing in a range of financial instruments on behalf of investors.",
        "A mutual fund offers a simple way to invest in a diversified portfolio, managed by financial experts for optimal performance.",
        "A mutual fund allows small or large investors to access a broad range of assets through a single investment product."
    ],
    "what is sip": [
        "A Systematic Investment Plan (SIP) is a way to invest a fixed amount regularly into mutual funds to build wealth over time.",
        "A SIP helps investors grow their money gradually by contributing a set sum every month into chosen mutual fund schemes.",
        "A SIP is a disciplined investment method where a fixed sum is automatically invested at regular intervals, promoting long-term wealth creation.",
        "A SIP allows consistent investing without market timing, helping investors average their costs and build a strong portfolio over the years.",
        "A SIP is an ideal tool for developing a regular investment habit, especially useful for long-term financial goals like retirement or education."
    ],
    "how do i invest in sip": [
        "To start a SIP, choose a mutual fund, complete KYC, and set up a fixed monthly investment through an online platform or app.",
        "Investing in a SIP involves selecting a mutual fund, setting an amount and frequency, and authorizing auto-debit from your bank account.",
        "Begin a SIP by signing up with an investment platform, completing your KYC verification, and choosing the scheme and date for regular investments.",
        "Start a SIP by picking a suitable fund, linking your bank account, and scheduling recurring monthly investments.",
        "Setting up a SIP is simple—register online with a fund house or app, select your fund, and enable auto-pay for regular contributions."
    ],
    "what is swp": [
        "A Systematic Withdrawal Plan (SWP) allows an investor to withdraw a fixed amount from a mutual fund investment at regular intervals.",
        "An SWP offers a structured way to receive periodic payouts from a mutual fund without redeeming the entire investment at once.",
        "An SWP helps generate a regular income stream by automatically withdrawing a chosen amount from your fund on a set schedule.",
        "An SWP provides steady cash flow, ideal for individuals seeking monthly income from their invested corpus while keeping the rest invested.",
        "An SWP is designed to allow consistent withdrawals from a mutual fund, making it useful for retirement or passive income planning."
    ],
    "how do i invest in swp": [
        "To start an SWP, invest in a mutual fund first, then submit a request for regular withdrawals through the fund house or investment platform.",
        "Set up an SWP by choosing the mutual fund, specifying the withdrawal amount and frequency, and confirming the schedule online or offline.",
        "Begin an SWP by logging into your investment account, selecting the fund, and defining how much and how often you want to withdraw.",
        "After investing in a mutual fund, activate an SWP by setting a regular withdrawal plan through the fund’s official website or app.",
        "Start an SWP by deciding the amount and interval for withdrawals, then initiating the request with your mutual fund provider."
    ],
    "what are bonds": [
        "A bond is a loan you give to a government or company, and in return, you receive regular interest payments and your money back at maturity.",
        "A bond is a fixed-income investment where the issuer borrows money from investors and pays interest over time until the principal is repaid.",
        "A bond works as a debt agreement between the issuer and the investor, offering predictable returns over a fixed time period.",
        "A bond allows investors to earn interest by lending money to entities like governments or corporations for a defined term.",
        "A bond is a relatively low-risk investment that generates stable income, making it suitable for conservative investors."
    ],
    "what is an emergency fund": [
        "An emergency fund is a financial safety net that covers unexpected expenses like medical emergencies, job loss, or urgent repairs.",
        "An emergency fund consists of savings reserved for unforeseen situations to avoid financial strain or the need for loans.",
        "An emergency fund provides quick access to cash in difficult times, helping you stay financially stable during emergencies.",
        "An emergency fund should ideally cover 3–6 months of living expenses and be kept in a highly liquid, safe account.",
        "An emergency fund is essential for financial security, giving peace of mind and protection from life’s uncertainties."
    ],
    "what is an etf": [
        "An Exchange-Traded Fund (ETF) is a type of investment fund that holds a collection of assets and trades on stock exchanges like shares.",
        "An ETF offers exposure to a range of assets—such as stocks, bonds, or commodities—while allowing intraday trading flexibility.",
        "An ETF is a low-cost, diversified investment product that combines the benefits of mutual funds with the trading features of stocks.",
        "An ETF tracks an index or sector and allows investors to buy or sell it anytime during market hours, just like regular shares.",
        "An ETF helps spread risk across multiple securities and is a popular choice for passive investors seeking broad market exposure."
    ],
    "what is diversification": [
        "Diversification is a risk management strategy that involves investing in different assets to reduce the impact of poor performance in any one area.",
        "Diversification spreads investments across various asset classes, sectors, or regions to lower overall portfolio risk.",
        "Diversification ensures that negative returns in one investment are balanced out by positive returns in others, leading to more stable growth.",
        "Diversification helps protect your capital by reducing dependence on the success of a single investment or asset type.",
        "Diversification improves the risk-return balance by combining assets that behave differently under various market conditions."
    ],
        "what is asset allocation": [
        "Asset allocation is the process of dividing your investments among different categories like stocks, bonds, and cash to balance risk and reward.",
        "Asset allocation means spreading your money across various asset types to match your financial goals, time horizon, and risk tolerance.",
        "Asset allocation involves choosing how much to invest in different asset classes to create a diversified and balanced portfolio.",
        "Asset allocation is a key strategy in investing that helps manage risk by not putting all money into one type of investment.",
        "Asset allocation is about deciding the right mix of investments to help grow wealth while protecting against major losses."
    ],
    "what is compounding": [
        "Compounding is the process where your money earns returns, and those returns also start earning, leading to exponential growth over time.",
        "Compounding means earning interest on both your original investment and the interest that accumulates over time.",
        "Compounding allows your wealth to grow faster because the gains you make begin to generate their own earnings.",
        "Compounding turns small, consistent investments into significant wealth by reinvesting the profits repeatedly.",
        "Compounding is the snowball effect of reinvesting earnings, which leads to much larger growth in the long run."
    ],
    "how much should i invest": [
        "The ideal investment amount depends on income, expenses, goals, and risk appetite, but even small regular investments can make a difference.",
        "Start investing with whatever amount is affordable consistently, and increase it as income grows to build long-term wealth.",
        "Invest an amount that doesn’t affect essential expenses and gradually increase it as you get more comfortable with the process.",
        "There’s no fixed amount—what matters is starting early and staying consistent, even with modest sums.",
        "Begin with what fits your budget without financial stress, and focus on growing that amount steadily over time."
    ],
    "what is inflation": [
        "Inflation is the rate at which the prices of goods and services increase, reducing the purchasing power of money over time.",
        "Inflation refers to the gradual rise in prices, which means your money buys less in the future than it does today.",
        "Inflation decreases the value of money, making it important to invest so your returns outpace rising costs.",
        "Inflation is the economic phenomenon where the cost of living increases, eroding the value of savings if not invested wisely.",
        "Inflation represents the loss of money's value over time, highlighting the importance of beating it through smart investing."
    ],
    "what is diversification in mutual funds": [
        "Diversification in mutual funds means investing across multiple assets or sectors to reduce overall portfolio risk.",
        "Mutual fund diversification helps lower risk by spreading investments so that poor performance in one area doesn’t impact the entire fund.",
        "Diversifying within mutual funds ensures that returns are not reliant on a single stock or sector, making investing safer.",
        "Mutual funds use diversification to balance risk and return by including a wide variety of assets in a single portfolio.",
        "Diversification in mutual funds allows exposure to many securities, providing stability and smoother performance over time."
    ],
    "what is a demat account": [
        "A Demat account is an electronic account that holds your stocks and other securities digitally instead of in physical form.",
        "A Demat account stores shares and investments safely in digital form, making buying, selling, and managing investments easier.",
        "A Demat account acts like a digital locker for securities, required for trading or investing in the stock market.",
        "A Demat account simplifies investing by keeping all your holdings in one place and enabling seamless online transactions.",
        "A Demat account is essential for stock market investing, allowing secure and paperless ownership of financial instruments."
    ],
    "what is kyc": [
        "KYC, or Know Your Customer, is the verification process to confirm your identity before you can open investment or financial accounts.",
        "KYC is a mandatory procedure where you submit identity and address proof to comply with legal and regulatory requirements before investing.",
        "KYC ensures that financial institutions verify who you are using documents like PAN, Aadhaar, and address proof.",
        "KYC helps prevent fraud and enables secure investing by confirming the identity of investors before transactions are allowed.",
        "KYC is a simple, one-time process that gives access to various investment products after verifying your details."
    ],
    "what is a financial goal": [
        "A financial goal is a specific target for managing money, such as saving for a home, retirement, or child’s education.",
        "A financial goal defines what you want to achieve with your money within a certain time frame, like buying a car or building a corpus.",
        "A financial goal helps give purpose to your investments by setting a timeline and target amount to reach.",
        "A financial goal is a milestone you plan for using your savings or investments, often categorized as short, medium, or long-term.",
        "A financial goal gives direction to your money decisions and helps in planning how much to invest and for how long."
    ],
    "how to set a financial goal": [
        "Start by identifying what you want to achieve, estimate the cost, decide the timeline, and choose the right investment strategy.",
        "To set a financial goal, define the purpose, calculate how much money is needed, and set a deadline to work toward it.",
        "Setting a financial goal involves choosing a target, breaking it into steps, and aligning your investments to meet that goal.",
        "Clearly define your goal, understand how much you’ll need, and plan your monthly investments to reach it in time.",
        "A financial goal is best set by figuring out your priorities, estimating future costs, and creating a savings or investment plan accordingly."
    ],
    "what is a credit score": [
        "A credit score is a number that represents how trustworthy you are when borrowing money, based on your repayment history and credit behavior.",
        "A credit score reflects your ability to repay loans or credit cards and helps banks decide whether to lend you money.",
        "A credit score is a key financial indicator used by lenders to judge how responsibly you’ve managed credit in the past.",
        "A credit score affects loan approval and interest rates—higher scores mean better chances of getting credit at lower rates.",
        "A credit score is calculated using your payment history, credit usage, and loan records, and it influences your financial credibility."
    ],
    "suggest some platforms to invest in shares/ stocks": [
        "Popular platforms to invest in shares include Zerodha, Groww, Upstox, Angel One, and ICICI Direct.",
        "You can start investing in stocks through trusted platforms like Zerodha, Groww, Angel One, Upstox, or HDFC Securities.",
        "Some good platforms for stock investing are Zerodha, Groww, Upstox, Angel One, and Motilal Oswal.",
        "Zerodha, Groww, and Upstox are widely used platforms that offer easy and secure ways to invest in the stock market.",
        "Top stock investment platforms in India include Zerodha, Groww, Angel One, Upstox, and ICICI Direct."
    ],
        "what is fd": [
        "A Fixed Deposit (FD) is a savings scheme where you deposit money for a fixed tenure and earn a guaranteed interest rate.",
        "FDs are low-risk investments offered by banks or NBFCs where your money earns interest over a fixed time period.",
        "With an FD, you lock in your money for a specific duration and earn returns at a pre-agreed interest rate.",
        "Fixed Deposits provide safety and stable returns, making them popular for conservative investors.",
        "An FD is a secure investment that helps grow your savings with fixed returns and minimal risk."
    ],
    "what is rd": [
        "A Recurring Deposit (RD) is a savings scheme where you deposit a fixed amount monthly and earn interest over time.",
        "RDs let you invest small sums regularly, making it easier to build a corpus with disciplined savings.",
        "With an RD, you commit to monthly deposits for a fixed tenure and receive interest similar to FDs.",
        "Recurring Deposits are ideal for those who want to save consistently and earn stable returns.",
        "An RD helps build a habit of saving monthly while earning interest, perfect for goal-based savings."
    ],
    "what is small cap, mid cap, large cap stock/funds": [
        "Large-cap stocks belong to well-established companies with large market capitalizations, mid-caps are medium-sized firms, and small-caps are younger or emerging companies.",
        "Stocks are categorized by market capitalization: large-cap (stable, blue-chip firms), mid-cap (growth potential), and small-cap (high risk, high reward).",
        "Large-cap stocks are usually safer and more stable, mid-caps balance growth and risk, while small-caps can be volatile but offer growth opportunities.",
        "Companies are classified by size—large-caps are industry leaders, mid-caps are growing businesses, and small-caps are relatively new or niche players.",
        "Large-cap stocks tend to be reliable, mid-caps offer growth, and small-caps carry higher risk but can generate strong returns if chosen wisely."
    ],
    "why to invest in stocks": [
        "Investing in stocks helps you build wealth over time through capital appreciation and dividends.",
        "Stocks offer the potential for higher returns compared to traditional savings or fixed-income products.",
        "By investing in the stock market, you become a part-owner in companies and benefit from their growth.",
        "Stock investments help beat inflation and grow your money faster than keeping it idle in a bank account.",
        "Over the long term, stock investing has historically provided some of the best returns for wealth creation."
    ],
    "what is nse": [
        "NSE stands for National Stock Exchange, one of India’s leading stock exchanges where securities are traded electronically.",
        "The National Stock Exchange (NSE) is a major platform for buying and selling shares and other financial instruments in India.",
        "NSE is known for its high-tech infrastructure, transparency, and benchmark index—Nifty 50.",
        "It’s one of the largest exchanges in India, offering a wide range of products including equities, derivatives, and bonds.",
        "The NSE provides a modern and efficient marketplace for investors to trade securities seamlessly."
    ],
    "what is bse": [
        "BSE stands for Bombay Stock Exchange, the oldest stock exchange in Asia and one of the largest in India.",
        "BSE is a premier Indian stock exchange headquartered in Mumbai, known for the Sensex index.",
        "Established in 1875, the BSE is a key platform for trading stocks and other securities in India.",
        "It’s a historic exchange that facilitates electronic trading of shares and financial instruments across India.",
        "BSE provides a reliable and regulated platform for companies to raise capital and for investors to trade efficiently."
    ],
    "what is the difference between nse bse": [
        "The main difference is that NSE's benchmark index is Nifty 50, while BSE uses Sensex; NSE also has higher trading volumes.",
        "NSE is more popular for derivatives trading, whereas BSE is known for its historical significance and broader company listings.",
        "Both are top Indian exchanges—NSE offers greater liquidity and faster execution; BSE is older with a larger number of listed companies.",
        "While both NSE and BSE allow stock trading, NSE generally sees more active participation and trades per day.",
        "NSE is preferred for options and futures trading, while BSE remains iconic for long-term investors and historical significance."
    ],
        "what is fd": [
        "A Fixed Deposit (FD) is a savings scheme where you deposit money for a fixed tenure and earn a guaranteed interest rate.",
        "FDs are low-risk investments offered by banks or NBFCs where your money earns interest over a fixed time period.",
        "With an FD, you lock in your money for a specific duration and earn returns at a pre-agreed interest rate.",
        "Fixed Deposits provide safety and stable returns, making them popular for conservative investors.",
        "An FD is a secure investment that helps grow your savings with fixed returns and minimal risk."
    ],
    "what is rd": [
        "A Recurring Deposit (RD) is a savings scheme where you deposit a fixed amount monthly and earn interest over time.",
        "RDs let you invest small sums regularly, making it easier to build a corpus with disciplined savings.",
        "With an RD, you commit to monthly deposits for a fixed tenure and receive interest similar to FDs.",
        "Recurring Deposits are ideal for those who want to save consistently and earn stable returns.",
        "An RD helps build a habit of saving monthly while earning interest, perfect for goal-based savings."
    ],
    "what is small cap, mid cap, large cap stock": [
        "Large-cap stocks belong to well-established companies with large market capitalizations, mid-caps are medium-sized firms, and small-caps are younger or emerging companies.",
        "Stocks are categorized by market capitalization: large-cap (stable, blue-chip firms), mid-cap (growth potential), and small-cap (high risk, high reward).",
        "Large-cap stocks are usually safer and more stable, mid-caps balance growth and risk, while small-caps can be volatile but offer growth opportunities.",
        "Companies are classified by size—large-caps are industry leaders, mid-caps are growing businesses, and small-caps are relatively new or niche players.",
        "Large-cap stocks tend to be reliable, mid-caps offer growth, and small-caps carry higher risk but can generate strong returns if chosen wisely."
    ],
    "why to invest in stock": [
        "Investing in stocks helps you build wealth over time through capital appreciation and dividends.",
        "Stocks offer the potential for higher returns compared to traditional savings or fixed-income products.",
        "By investing in the stock market, you become a part-owner in companies and benefit from their growth.",
        "Stock investments help beat inflation and grow your money faster than keeping it idle in a bank account.",
        "Over the long term, stock investing has historically provided some of the best returns for wealth creation."
    ],
    "what is nse": [
        "NSE stands for National Stock Exchange, one of India’s leading stock exchanges where securities are traded electronically.",
        "The National Stock Exchange (NSE) is a major platform for buying and selling shares and other financial instruments in India.",
        "NSE is known for its high-tech infrastructure, transparency, and benchmark index—Nifty 50.",
        "It’s one of the largest exchanges in India, offering a wide range of products including equities, derivatives, and bonds.",
        "The NSE provides a modern and efficient marketplace for investors to trade securities seamlessly."
    ],
    "what is bse": [
        "BSE stands for Bombay Stock Exchange, the oldest stock exchange in Asia and one of the largest in India.",
        "BSE is a premier Indian stock exchange headquartered in Mumbai, known for the Sensex index.",
        "Established in 1875, the BSE is a key platform for trading stocks and other securities in India.",
        "It’s a historic exchange that facilitates electronic trading of shares and financial instruments across India.",
        "BSE provides a reliable and regulated platform for companies to raise capital and for investors to trade efficiently."
    ],
    "diff between nse bse": [
        "The main difference is that NSE's benchmark index is Nifty 50, while BSE uses Sensex; NSE also has higher trading volumes.",
        "NSE is more popular for derivatives trading, whereas BSE is known for its historical significance and broader company listings.",
        "Both are top Indian exchanges—NSE offers greater liquidity and faster execution; BSE is older with a larger number of listed companies.",
        "While both NSE and BSE allow stock trading, NSE generally sees more active participation and trades per day.",
        "NSE is preferred for options and futures trading, while BSE remains iconic for long-term investors and historical significance."
    ],
    "what is a balanced mutual fund": [
        "A balanced mutual fund is a type of fund that invests in both stocks and bonds to provide a mix of growth and stability.",
        "Balanced mutual funds aim to reduce risk by diversifying across equity and debt instruments, making them suitable for moderate-risk investors.",
        "These funds maintain a blend of equity for higher returns and fixed-income securities for stability, ensuring a balanced portfolio.",
        "Investing in a balanced fund helps investors enjoy stock market gains while reducing volatility with bond allocations.",
        "Balanced funds are ideal for those who want exposure to equities without taking excessive risks, as they offer a mix of growth and income."
    ],
    "what is a REIT": [
        "A Real Estate Investment Trust (REIT) is a company that owns and manages income-generating real estate properties.",
        "REITs allow investors to invest in real estate without directly owning properties by buying shares in real estate-focused companies.",
        "These funds generate returns from rental income, property appreciation, and capital gains, making them a way to invest in real estate passively.",
        "REITs function like mutual funds, pooling investor money to buy and manage commercial properties such as malls, offices, and hotels.",
        "They provide an opportunity to earn real estate income without the hassle of property management, offering liquidity and regular dividends."
    ],
    "what is portfolio diversification": [
        "Portfolio diversification is the strategy of spreading investments across different asset types to reduce risk.",
        "By diversifying, investors ensure that a decline in one asset does not significantly impact the overall portfolio performance.",
        "A well-diversified portfolio includes a mix of stocks, bonds, gold, and other assets, balancing risk and returns.",
        "Diversification helps protect against market volatility by investing in various sectors, geographies, and asset classes.",
        "It’s a key principle of investing that reduces risk while aiming for stable and consistent long-term returns."
    ],
    "what is asset": [
    "An asset is anything of value that can be owned or controlled to produce value or benefit.",
    "In investing, assets include things like stocks, bonds, real estate, and commodities.",
    "Assets are categorized as tangible (like property) or intangible (like patents or stocks).",
    "They are a fundamental part of a portfolio and play a key role in building wealth over time.",
    "Assets can appreciate or depreciate in value, affecting an investor’s net worth and financial goals."
    ],

    "what is an index fund": [
        "An index fund is a type of mutual fund or ETF that mimics the performance of a stock market index like Nifty 50 or Sensex.",
        "These funds passively track an index, meaning they don’t require active management and usually have lower costs.",
        "Investing in an index fund allows for broad market exposure, making it a simple and effective way to build wealth over time.",
        "Index funds are popular among long-term investors because they provide diversification and typically outperform actively managed funds over time.",
        "Since they follow a specific index, their returns depend on how that index performs, eliminating the need for stock picking."
    ],"what is liability": [
    "A liability is a financial obligation or debt that a person or organization owes to another party.",
    "Common examples include loans, credit card debt, mortgages, and unpaid bills.",
    "Liabilities are recorded on the balance sheet and represent money that must be paid in the future.",
    "They are typically categorized as current (short-term) or long-term based on when they are due.",
    "Managing liabilities is essential for maintaining financial health and avoiding excessive debt."
],

    "hi": ["Hey there! ", "Hello! How can I assist you today?", "Hi! Need help with finance or stocks?"],
    "hello": ["Hello! ", "Hey! How can I help?", "Hi there! What can I do for you today?"],
    "thanks": ["You're welcome! ", "Glad to help! ", "Anytime! "],
    "thankyou": ["You're very welcome! ", "No problem at all!", "Happy to help!"],
    "thank you": ["You're very welcome! ", "No problem at all!", "Happy to help!"],
    "sorry": ["No worries at all!", "It’s okay!", "All good! "],
    "okay": ["Got it! ", "Cool ", "Alright! Let me know if you need anything else."]
}

# Plan question flow
plan_questions = [
    "1. What's your age?",
    "2. What is your monthly income (in ₹)?",
    "3. How much do you save per month (in ₹)?",
    "4. What's your risk tolerance? (low / medium / high)",
    "5. Investment horizon? (short / long term)",
    "6. Are you comfortable investing in stocks? (yes / no)",
    "7. Do you expect a big expense in the next 1-3 years? (yes / no)",
    "8. Do you have an emergency fund? (yes / no)",
    "9. Do you already invest in mutual funds or stocks? (yes / no)",
    "10. Do you have any ongoing loans or EMIs? (yes / no)",
    "11. What is your total monthly EMI payment (in ₹)?",
    "12. What is your current investment knowledge? (beginner / intermediate / advanced)",
    "13. How do you prefer to invest? (monthly / lump sum / both)"
]


portfolio_questions = [
    "1. What's your investment goal? (wealth building / retirement / passive income / saving for a major goal)",
    "2. What's your preferred investment type? (stocks / mutual funds / mix / ETFs / real estate)",
    "3. How much can you invest right now (in ₹)?",
    "4. How long do you plan to stay invested? (short / medium / long term)",
    "5. Are you open to global or alternative assets like US stocks, REITs, or gold? (yes / no)",
    "6. Would you prefer active management or passive index investing? (active / passive / mix)",
    "7. Do you want regular income from investments or growth over time? (income / growth / both)",
    "8. How involved do you want to be? (hands-on / semi-active / fully automated)",
    "9. Do you already hold any major assets? (real estate / gold / stocks / none)",
    "10. Do you want your portfolio to include insurance or health-linked investments? (yes / no)",
    "11. How often do you plan to review or rebalance your portfolio? (monthly / quarterly / yearly / rarely)"
]



def answer_faq(user_input):
    user_input = user_input.lower()
    matches = get_close_matches(user_input, finance_faq.keys(), n=1, cutoff=0.6)
    if matches:
        return random.choice(finance_faq[matches[0]])
    return "Sorry, I don't have an answer for that yet."

import requests

ALPHA_VANTAGE_API_KEY = "0EDEKUT1C724LEXC"
TWELVE_DATA_API_KEY = "73aba4453d4140f0a1882724f747c21e"

STOCK_NAME_TO_TICKER = {
    # US Companies
    "apple": "AAPL", "microsoft": "MSFT", "tesla": "TSLA", "amazon": "AMZN", "google": "GOOGL",
    "alphabet": "GOOGL", "meta": "META", "facebook": "META", "nvidia": "NVDA", "netflix": "NFLX",
    "paypal": "PYPL", "adobe": "ADBE", "intel": "INTC", "amd": "AMD", "uber": "UBER", "zoom": "ZM",
    "salesforce": "CRM", "oracle": "ORCL", "cisco": "CSCO", "spotify": "SPOT", "walmart": "WMT",
    "mcdonalds": "MCD", "nike": "NKE", "starbucks": "SBUX", "boeing": "BA", "coca cola": "KO",
    "pepsi": "PEP", "disney": "DIS", "chevron": "CVX", "exxonmobil": "XOM", "johnson & johnson": "JNJ",
    "pfizer": "PFE", "moderna": "MRNA", "goldman sachs": "GS", "jpmorgan": "JPM",
    "bank of america": "BAC", "visa": "V", "mastercard": "MA",

  # Indian Companies (Twelve Data uses BSE format)
    "reliance": "RELIANCE.BSE",
    "tcs": "TCS.BSE",
    "infosys": "INFY.BSE",
    "hdfc bank": "HDFCBANK.BSE",
    "icici bank": "ICICIBANK.BSE",
    "state bank of india": "SBIN.BSE",
    "hcl": "HCLTECH.BSE",
    "larsen & toubro": "LT.BSE",
    "itc": "ITC.BSE",
    "axis bank": "AXISBANK.BSE",
    "bharat petroleum": "BPCL.BSE",
    "hindustan unilever": "HINDUNILVR.BSE",
    "maruti": "MARUTI.BSE",
    "tata motors": "TATAMOTORS.BSE",
    "tata steel": "TATASTEEL.BSE",
    "asian paints": "ASIANPAINT.BSE",
    "sun pharma": "SUNPHARMA.BSE",
    "ultratech cement": "ULTRACEMCO.BSE",
    "tech mahindra": "TECHM.BSE"
}

def get_stock_price(query):
    query = query.lower()
    stock_keywords = [
        "stock price of", "price of", "share price of", "stock price",
        "stock price for", "price for", "current price of", "current price for"
    ]
    for keyword in stock_keywords:
        if keyword in query:
            company_name = query.split(keyword)[-1].strip()
            break
    else:
        return "❌ Please include a phrase like 'stock price of' in your query."

    # Get Ticker
    company_key = company_name.lower()
    ticker = STOCK_NAME_TO_TICKER.get(company_key, company_name.upper())

    try:
        # Check if it's an Indian stock (contains .NSE)
        if ".NSE" in ticker:
            td_url = "https://api.twelvedata.com/time_series"
            td_params = {
                "symbol": ticker,
                "interval": "1min",
                "apikey": TWELVE_DATA_API_KEY
            }
            td_response = requests.get(td_url, params=td_params)
            td_data = td_response.json()

            if "values" in td_data:
                price = td_data["values"][0]["close"]
                return f"🇮🇳 📈 {ticker} current stock price is ₹{price}"
            else:
                return f"❌ Twelve Data Error: {td_data.get('message', 'Unknown error')}"

        # Else: Global stock
        av_url = "https://www.alphavantage.co/query"
        av_params = {
            "function": "GLOBAL_QUOTE",
            "symbol": ticker,
            "apikey": ALPHA_VANTAGE_API_KEY
        }
        av_response = requests.get(av_url, params=av_params)
        av_data = av_response.json()

        quote = av_data.get("Global Quote", {})
        price = quote.get("05. price")

        if price:
            return f"🌍 📈 {ticker} current stock price is {price} USD"
        else:
            return f"❌ Alpha Vantage Error: {av_data.get('Note') or 'Invalid symbol or rate limit hit.'}"

    except Exception as e:
        return f"❌ Error fetching stock price: {str(e)}"

def is_in_plan_mode(session):
    return session.get("in_plan_mode", False)

def update_plan_session(session, user_input):
    idx = session.get("plan_question_index", 0)
    session.setdefault("plan_answers", []).append(user_input)
    session["plan_question_index"] = idx + 1

def reset_plan(session):
    session["in_plan_mode"] = False
    session["plan_question_index"] = 0
    session["plan_answers"] = []

def is_in_portfolio_mode(session):
    return session.get("in_portfolio_mode", False)

def update_portfolio_session(session, user_input):
    idx = session.get("portfolio_question_index", 0)
    session.setdefault("portfolio_answers", []).append(user_input)
    session["portfolio_question_index"] = idx + 1

def reset_portfolio(session):
    session["in_portfolio_mode"] = False
    session["portfolio_question_index"] = 0
    session["portfolio_answers"] = []

def get_response(message, session):
    message = message.strip().lower()
    time.sleep(1.60)

    # Start planning session
    if message == "plan" and not is_in_plan_mode(session):
        session["in_plan_mode"] = True
        session["plan_question_index"] = 0
        session["plan_answers"] = []
        return plan_questions[0]

    # Continue planning session
    if is_in_plan_mode(session):
        update_plan_session(session, message)
        idx = session["plan_question_index"]

        if idx < len(plan_questions):
            return plan_questions[idx]
        else:
            plan = generate_plan(session["plan_answers"])
            reset_plan(session)
            return plan

    # Start portfolio session
    if message == "portfolio" and not is_in_portfolio_mode(session):
        session["in_portfolio_mode"] = True
        session["portfolio_question_index"] = 0
        session["portfolio_answers"] = []
        return portfolio_questions[0]

    # Continue portfolio session
    if is_in_portfolio_mode(session):
        update_portfolio_session(session, message)
        idx = session["portfolio_question_index"]

        if idx < len(portfolio_questions):
            return portfolio_questions[idx]
        else:
            portfolio = generate_portfolio(session["portfolio_answers"])
            reset_portfolio(session)
            return portfolio

    stock = get_stock_price(message)
    if stock and not stock.startswith("❌"):
        return stock

    faq = answer_faq(message)
    if faq:
        return faq


    return " I'm not sure about that. Try asking about SIPs, stocks, or type 'plan' to build an investment strategy or 'portfolio' for a portfolio suggestion."


import random
import random

def generate_plan(answers):
    try:
        age = int(answers[0])
        income = float(answers[1])
        savings = float(answers[2])
        risk = answers[3].lower()
        horizon = answers[4].lower()
        stocks_ok = answers[5].lower()
        big_expense = answers[6].lower()
        emergency_fund = answers[7].lower()
        existing_investments = answers[8].lower()
        has_loans = answers[9].lower()
        knowledge = answers[10].lower()
        invest_mode = answers[11].lower()
    except Exception:
        return "⚠️ Oops! Something went wrong while processing your answers."

    allocation = {}
    recommendations = []

    # Emergency fund
    if emergency_fund == "no":
        allocation["Emergency Fund (Bank FD or Liquid Fund)"] = 20
        emergency_pool = [
            "- Build an emergency fund using SBI Liquid Fund or HDFC Overnight Fund.",
            "- Park funds in a liquid or overnight fund to handle emergencies.",
            "- Start with an FD or a liquid mutual fund like ICICI Liquid Fund for emergencies.",
            "- Ensure liquidity with a short-term FD or Axis Overnight Fund.",
            "- Emergency funds should be easily accessible—consider a savings-linked sweep-in FD.",
            "- Nippon Liquid Fund or IDFC Overnight Fund are good options for emergency buffers.",
            "- Create a separate emergency account with automatic monthly top-ups.",
            "- Use a recurring deposit for a disciplined emergency fund strategy."
        ]
        recommendations.append(random.choice(emergency_pool))

    # Short term needs
    if big_expense == "yes":
        allocation["Short-Term Debt Funds"] = 20
        short_term_pool = [
            "- Use low-risk debt funds like ICICI Short Term Fund for near-term needs.",
            "- Consider short-term bond funds to keep money safe yet accessible.",
            "- Avoid equity; park funds in short-term mutual funds like Axis Short Term Fund.",
            "- Short-term target? Go for SBI Magnum Low Duration Fund.",
            "- Consider ultra short duration funds like HDFC Ultra Short Fund.",
            "- Franklin Savings Fund is a good fit for 1–3 year goals.",
            "- Nippon Low Duration Fund balances return and risk for short horizons.",
            "- Use laddered FDs for predictable cash flow."
        ]
        recommendations.append(random.choice(short_term_pool))

    # Risk profile-based allocations
    if risk == "low":
        allocation["Debt Mutual Funds"] = 40
        allocation["Gold ETFs"] = 10
        allocation["REITs or Bonds"] = 10
        low_risk_pool = [
            "- Axis Treasury Advantage Fund is a safe debt mutual fund option.",
            "- ICICI Corporate Bond Fund offers steady returns.",
            "- HDFC Short Term Debt Fund is good for low-risk investors.",
            "- Gold ETFs like Nippon India Gold ETF act as good inflation hedges.",
            "- Consider gold via mutual funds or ETFs for long-term balance.",
            "- Try Bharat Bond ETF or Embassy REIT for fixed income.",
            "- Edelweiss Bharat Bond ETF can offer stable returns with low risk.",
            "- Invest in Sovereign Gold Bonds for tax benefits and safety.",
            "- Choose SBI Magnum Gilt Fund for secure government-backed returns.",
            "- Diversify with Kotak Gold Fund and Axis Strategic Bond Fund.",
            "- UTI Corporate Bond Fund provides a conservative income stream.",
            "- Add PPF or EPF contributions for long-term low-risk exposure."
        ]
        recommendations += random.sample(low_risk_pool, 3)

    elif risk == "medium":
        allocation["Equity Mutual Funds"] = 50
        allocation["Debt Funds"] = 20
        allocation["REITs or Gold"] = 10
        medium_risk_pool = [
            "- Invest in hybrid funds like HDFC Balanced Advantage Fund.",
            "- Add multi-asset funds for a balanced approach.",
            "- Consider flexi-cap funds like Parag Parikh Flexi Cap.",
            "- Use REITs for stable rental income, like Mindspace Business Parks REIT.",
            "- Mix equity and debt to balance growth and stability.",
            "- Grow wealth with balanced funds like ICICI Multi-Asset Fund.",
            "- Include DSP Dynamic Asset Allocation Fund for market adaptability.",
            "- SBI Balanced Advantage Fund is good for moderate-risk investors.",
            "- Try Kotak Equity Hybrid Fund to hedge volatility.",
            "- Use Axis Multi-Asset Allocation Fund for a diverse approach.",
            "- Combine HDFC Hybrid Equity Fund with Gold ETFs for hedging."
        ]
        recommendations += random.sample(medium_risk_pool, 3)

    else:  # High risk
        if age < 35:
            allocation["Stocks"] = 50
            stock_pool = [
                "- Explore stocks like TCS, Infosys, HDFC Bank, or ETFs like Nifty50 ETF.",
                "- Start with index-based ETFs or large-cap stocks.",
                "- Direct equity suits young, risk-tolerant investors.",
                "- Consider SIPs in large-cap ETFs like Motilal Oswal Nifty 50 ETF.",
                "- Use a brokerage app like Zerodha to explore direct equity options.",
                "- Add mid-cap exposure gradually with stocks like Tata Elxsi or Persistent.",
                "- Use ETF baskets like Nifty Next 50 for diversification.",
                "- Try smallcases focused on themes like digital or green energy."
            ]
            recommendations.append(random.choice(stock_pool))

        allocation["Equity Mutual Funds"] = 30
        allocation["Crypto (optional)"] = 5
        crypto_pool = [
            "- Consider Bitcoin or Ethereum via CoinSwitch, but only a small %. ",
            "- Explore crypto cautiously—keep exposure under 5%.",
            "- Crypto is optional—invest only what you can afford to lose.",
            "- If interested in crypto, start small with regulated platforms.",
            "- Use SIPs in crypto to reduce volatility risk.",
            "- Add a small stake in crypto via CoinDCX or WazirX.",
            "- Avoid overexposure—crypto should be less than 5% of your net worth."
        ]
        recommendations.append("🔸 Grow wealth via mutual funds like Quant Active Fund.")
        recommendations.append(random.choice(crypto_pool))

    # If not comfortable with stocks
    if stocks_ok == "no" and "Stocks" in allocation:
        allocation["Equity Mutual Funds"] = allocation.get("Equity Mutual Funds", 0) + allocation.pop("Stocks")
        recommendations.append("Since you're not comfortable with stocks, focus on equity mutual funds instead.")

    # Fill up if less than 100% allocated
    total_alloc = sum(allocation.values())
    if total_alloc < 100:
        allocation["Safe Funds (FD or Liquid Fund)"] = 100 - total_alloc

    # Build the plan text
    plan_text = " **Your Recommended Investment Plan:**\n"
    for asset, percent in allocation.items():
        amount = (savings * percent) / 100
        plan_text += f" - {asset}: ₹{amount:.2f} ({percent}%)\n"

    plan_text += "\n **Investment Suggestions:**\n" + "\n".join(recommendations)

    # Smart final tips
    plan_text += "\n\n **Final Tips:**"
    if emergency_fund == "no":
        plan_text += "\n- Build an emergency fund ASAP to cover 3–6 months of expenses."
    if big_expense == "yes":
        plan_text += "\n- Keep some funds liquid for upcoming expenses."
    if has_loans == "yes":
        plan_text += "\n- Prioritize clearing high-interest debt while investing."
    if invest_mode in ["sip", "monthly sip"]:
        plan_text += "\n- Stay consistent with your SIPs for long-term gains."
    if invest_mode == "lump sum":
        plan_text += "\n- Avoid timing the market—invest lump sums in staggered manner (STP)."
    if knowledge == "beginner":
        plan_text += "\n- Stick to index funds or balanced mutual funds until you're more confident."
    if knowledge == "advanced":
        plan_text += "\n- Explore direct equity, sector funds, or global ETFs if you're experienced."
    if horizon == "long term":
        plan_text += "\n- Stay invested long term to benefit from compounding and market growth."
    if risk == "low":
        plan_text += "\n- Review your debt fund returns periodically and rebalance if needed."
    if risk == "high":
        plan_text += "\n- High-risk investments need regular tracking—set a review schedule."

    return plan_text



import random

# Tip buckets for dynamic responses
TIP_POOL = {
    "sips": [
        "- SIPs help build discipline and make investing stress-free.",
        "- Start small with SIPs and gradually increase as your income grows.",
        "- SIPs enable rupee-cost averaging, which minimizes the impact of market volatility.",
        "- SIPs instill a habit of consistent saving and long-term wealth creation.",
        "- Choose SIP dates close to your salary credit date for consistency.",
        "- Automate your SIPs to stay consistent without emotional bias.",
        "- Use top-up SIPs to increase your monthly contribution annually.",
        "- SIPs in balanced funds can be a good start for new investors.",
        "- Delaying SIPs delays compounding—start today even if the amount is small.",
        "- Use SIP calculators to set realistic goals and timelines."
    ],
    "rebalance": [
        "- Rebalance at least once a year to maintain ideal asset allocation.",
        "- Rebalancing ensures your portfolio doesn’t drift from your risk profile.",
        "- Booking profits from over-performing assets helps manage overall risk.",
        "- A periodic rebalance prevents overexposure to volatile assets.",
        "- You can use calendar-based (yearly) or threshold-based (5–10% drift) rebalancing.",
        "- Consider rebalancing every 6 months if your portfolio is highly aggressive.",
        "- Use a goal-based rebalancing approach as you get closer to the target.",
        "- Rebalancing reduces the emotional temptation to chase returns.",
        "- Keep an eye on asset weightage rather than returns while rebalancing.",
        "- Tools like Kuvera or Zerodha Coin can help automate your rebalancing process."
    ],
    "stocks": [
        "- Invest in fundamentally strong, large-cap companies with steady returns.",
        "- Diversify across sectors to reduce concentration risk in your stock portfolio.",
        "- Avoid penny stocks or hype-driven companies without due diligence.",
        "- Use tools like Screener or TickerTape to analyze company fundamentals.",
        "- Keep emotions in check—follow a disciplined buy-and-hold strategy.",
        "- Track quarterly earnings and management commentary for your stocks.",
        "- Use the 'coffee can' strategy: buy quality, hold long term.",
        "- Don't ignore taxes—long-term equity gains above ₹1L are taxable.",
        "- Keep 15–20 stocks max to manage risk without diluting returns.",
        "- Avoid reacting to daily news cycles—focus on business fundamentals."
    ],
    "mutual_funds": [
        "- Choose funds with consistent 3–5 year performance, not just short-term gains.",
        "- Check for expense ratio and fund manager tenure before selecting a fund.",
        "- Avoid investing in too many funds; 3–4 good ones are enough.",
        "- Use direct plans instead of regular ones to save on commission charges.",
        "- Focus on funds with lower volatility if you’re risk-averse.",
        "- Large-cap funds are good for stability; mid/small caps for growth.",
        "- Review fund category every 6–12 months to ensure it aligns with your risk profile.",
        "- Avoid NFOs unless you clearly understand their strategy.",
        "- Use platforms like Value Research or Morningstar for in-depth comparisons.",
        "- Don't chase past returns—look for consistency and fund house credibility."
    ],
    "global": [
        "- Global investing protects you from local market volatility and currency risk.",
        "- Exposure to tech giants like Apple, Google, and Microsoft diversifies growth.",
        "- International funds offer a hedge during domestic economic downturns.",
        "- Keep global exposure to around 10–15% to balance growth and risk.",
        "- ETFs like Nasdaq 100 or S&P 500 Index are great starting points for global investing.",
        "- Dollar-denominated assets provide inflation and currency protection.",
        "- Global investing offers access to innovation sectors like AI, biotech, and green energy.",
        "- Use fund-of-funds if you're unsure about direct international investing.",
        "- Consider currency conversion costs and taxation on foreign funds.",
        "- Combine global and Indian assets to create a truly diversified portfolio."
    ],
    "passive": [
        "- Passive investing is low-cost, transparent, and ideal for long-term compounding.",
        "- Index funds usually outperform many active funds over the long term.",
        "- Passive funds avoid fund manager bias and emotional decision-making.",
        "- Stick to broad-based index funds like Nifty 50, Nifty Next 50, or S&P 500.",
        "- For beginners, passive investing provides simplicity and strong diversification.",
        "- Passive investing is ideal for investors who prefer minimal involvement.",
        "- Choose funds with low tracking error and consistent AUM growth.",
        "- Great for salaried individuals who want automation and low effort.",
        "- Passive investing suits goal-based planning with a 5–10 year horizon.",
        "- Even with passive funds, review performance at least once a year."
    ],
    "active": [
        "- Active funds aim to outperform the market but come with higher fees.",
        "- Analyze fund manager’s track record before trusting active strategies.",
        "- Active funds work well in less efficient markets like small-cap and mid-cap segments.",
        "- Monitor active funds regularly to ensure they still justify their higher cost.",
        "- Look for alpha-generating active funds in hybrid or thematic categories.",
        "- Consider sectoral or thematic funds only if you understand the industry cycle.",
        "- Avoid high-churn active funds that create unnecessary transaction costs.",
        "- Active funds are ideal if you want to capture short-term opportunities.",
        "- Combine active and passive strategies for optimal results.",
        "- Don't fall for marketing—evaluate fund performance independently."
    ]
}


def generate_portfolio(answers):
    try:
        goal = answers[0].strip().lower()
        type_pref = answers[1].strip().lower()
        amount = float(answers[2])
        horizon = answers[3].strip().lower()
        global_opt = answers[4].strip().lower()
        mgmt_style = answers[5].strip().lower()
        income_or_growth = answers[6].strip().lower()
        involvement = answers[7].strip().lower()
        existing_assets = answers[8].strip().lower()
        wants_insurance = answers[9].strip().lower()
        review_freq = answers[10].strip().lower()
    except:
        return "⚠️ Sorry, we couldn't process your inputs. Please try again."

    allocation = {}
    suggestions = []

    # Goal-based base allocation
    if goal == "retirement":
        allocation = {"Equity Mutual Funds": 50, "Debt Funds": 30, "REITs or Gold": 10}
        suggestions += [
            "- Consider HDFC Retirement Fund and ICICI Balanced Advantage Fund.",
            "- Mix debt and equity for stability and long-term growth."
        ]
    elif goal == "passive income":
        allocation = {"REITs & Dividend Stocks": 30, "Debt Funds": 40, "Balanced Funds": 20}
        suggestions += [
            "- Embassy or Mindspace REIT can help with steady rental income.",
            "- Dividend stocks like ITC or Coal India work well for passive income."
        ]
    elif goal == "saving for a major goal":
        allocation = {"Balanced Funds": 40, "Debt Funds": 30, "Gold ETFs or Liquid Funds": 10}
        suggestions += [
            "- Use balanced advantage funds to manage risk while targeting your goal.",
            "- Gold ETFs or FDs can provide liquidity closer to the goal timeline."
        ]
    else:  # Wealth building
        allocation = {"Equity Mutual Funds": 60, "Stocks": 20, "Gold ETFs or REITs": 10}
        suggestions += [
            "- Parag Parikh Flexi Cap and Quant Active are great for long-term wealth.",
            "- If comfortable, explore quality large-cap stocks like TCS or Infosys."
        ]

    # Horizon-based adjustment
    if horizon == "short":
        allocation = {"Debt Funds": 50, "Liquid Funds or FD": 30}
        suggestions.append("- Avoid equity for short-term goals; stick with debt or FDs.")
    elif horizon == "medium":
        allocation["Hybrid Mutual Funds"] = 15
        suggestions.append("- Add hybrid funds like ICICI Balanced Advantage Fund.")
    elif horizon == "long":
        allocation["Mid & Small Cap Funds"] = 10
        suggestions.append("- Consider small-cap funds for aggressive long-term returns.")

    # Global allocation
    if global_opt == "yes":
        allocation["International Funds"] = 10
        suggestions.append("🔸 Add global exposure via Motilal Oswal Nasdaq 100 or S&P 500 Index Fund.")

    # Income or Growth
    if income_or_growth == "income":
        allocation["Debt Funds"] = allocation.get("Debt Funds", 0) + 10
        suggestions.append("- Add income-generating funds or dividend-paying stocks.")
    elif income_or_growth == "growth":
        allocation["Equity Mutual Funds"] = allocation.get("Equity Mutual Funds", 0) + 10
        suggestions.append("- Prioritize growth-oriented equity mutual funds.")
    elif income_or_growth == "both":
        suggestions.append("- Balance your portfolio with a mix of equity and income sources.")

    # Involvement level
    if involvement == "hands-on":
        suggestions.append("- Track stocks regularly and rebalance your portfolio every quarter.")
    elif involvement == "semi-active":
        suggestions.append("- Use apps like Zerodha or Groww to automate some tracking.")
    else:  # fully automated
        suggestions.append("- Choose robo-advisors or index funds for hassle-free investing.")

    # Existing asset consideration
    if existing_assets != "none":
        suggestions.append(f"- Consider how your existing {existing_assets} holdings affect diversification.")

    # Insurance consideration
    if wants_insurance == "yes":
        suggestions.append("- Explore term plans or ULIPs that offer basic insurance + investment.")

    # Rebalancing frequency
    if review_freq in ["monthly", "quarterly"]:
        suggestions.append("- Set calendar reminders to review and rebalance your portfolio.")
    elif review_freq == "yearly":
        suggestions.append("- Rebalancing annually can help reduce volatility.")
    else:
        suggestions.append("- Avoid neglecting your investments—review at least once a year.")

    # Respect user preference
    if type_pref == "mutual funds":
        if "Stocks" in allocation:
            allocation["Equity Mutual Funds"] += allocation.pop("Stocks")
    elif type_pref == "stocks":
        if "Equity Mutual Funds" in allocation:
            allocation["Stocks"] = allocation.pop("Equity Mutual Funds")

    # Fill gap to 100%
    total_percent = sum(allocation.values())
    if total_percent < 100:
        allocation["Liquid Funds / Buffer"] = 100 - total_percent

    # Format result
    result = "**Your Portfolio Allocation:**\n"
    for k, v in allocation.items():
        invested = (amount * v) / 100
        result += f" - {k}: ₹{invested:.2f} ({v}%)\n"

    result += "\n**Investment Suggestions:**\n" + "\n".join(suggestions)

    # Dynamic Tips
    result += "\n\n**Tips:**"
    if "Equity Mutual Funds" in allocation or "Debt Funds" in allocation:
        result += "\n" + random.choice(TIP_POOL["sips"])
    if len(allocation) >= 3:
        result += "\n" + random.choice(TIP_POOL["rebalance"])
    else:
        result += "\n- Review your portfolio once every 6–12 months."

    if type_pref == "stocks":
        result += "\n" + random.choice(TIP_POOL["stocks"])
    elif type_pref == "mutual funds":
        result += "\n" + random.choice(TIP_POOL["mutual_funds"])
    else:
        result += "\n- Mix mutual funds and stocks to reduce risk and improve returns."

    if global_opt == "yes":
        result += "\n" + random.choice(TIP_POOL["global"])
    if mgmt_style == "passive":
        result += "\n" + random.choice(TIP_POOL["passive"])
    else:
        result += "\n" + random.choice(TIP_POOL["active"])

    result += "\n- Link every investment to a financial goal for better clarity."

    return result
