{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 43,
   "id": "a0469576-f7db-421c-bdd7-6af569768827",
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "Defaulting to user installation because normal site-packages is not writeable\n",
      "Requirement already satisfied: nltk in c:\\programdata\\anaconda3\\lib\\site-packages (3.9.2)\n",
      "Requirement already satisfied: beautifulsoup4 in c:\\programdata\\anaconda3\\lib\\site-packages (4.13.5)\n",
      "Requirement already satisfied: click in c:\\programdata\\anaconda3\\lib\\site-packages (from nltk) (8.2.1)\n",
      "Requirement already satisfied: joblib in c:\\programdata\\anaconda3\\lib\\site-packages (from nltk) (1.5.2)\n",
      "Requirement already satisfied: regex>=2021.8.3 in c:\\users\\visakh h s\\appdata\\roaming\\python\\python313\\site-packages (from nltk) (2026.5.9)\n",
      "Requirement already satisfied: tqdm in c:\\programdata\\anaconda3\\lib\\site-packages (from nltk) (4.67.1)\n",
      "Requirement already satisfied: soupsieve>1.2 in c:\\programdata\\anaconda3\\lib\\site-packages (from beautifulsoup4) (2.5)\n",
      "Requirement already satisfied: typing-extensions>=4.0.0 in c:\\programdata\\anaconda3\\lib\\site-packages (from beautifulsoup4) (4.15.0)\n",
      "Requirement already satisfied: colorama in c:\\programdata\\anaconda3\\lib\\site-packages (from click->nltk) (0.4.6)\n"
     ]
    }
   ],
   "source": [
    "#install libraries\n",
    "!pip install nltk beautifulsoup4"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 44,
   "id": "bdc16cfd-698e-4892-b06e-f87e2da2e604",
   "metadata": {},
   "outputs": [],
   "source": [
    "import sys\n",
    "from pathlib import Path\n",
    "\n",
    "SCRIPTS_DIR = Path.cwd() / \"scripts\"\n",
    "\n",
    "if str(SCRIPTS_DIR) not in sys.path:\n",
    "    sys.path.insert(0, str(SCRIPTS_DIR))"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 45,
   "id": "93017f13-5534-4e7d-8277-c9fe14bcbc72",
   "metadata": {},
   "outputs": [],
   "source": [
    "import re\n",
    "import pandas as pd\n",
    "from bs4 import BeautifulSoup\n",
    "\n",
    "import nltk\n",
    "from nltk.corpus import stopwords\n",
    "from nltk.stem import WordNetLemmatizer\n",
    "\n",
    "from config import MASTER_DATASET\n",
    "from logger import logger"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 46,
   "id": "6d137847-d873-4de2-a791-b20412624371",
   "metadata": {},
   "outputs": [
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "[nltk_data] Downloading package wordnet to C:\\Users\\Visakh H\n",
      "[nltk_data]     S\\AppData\\Roaming\\nltk_data...\n",
      "[nltk_data]   Package wordnet is already up-to-date!\n",
      "[nltk_data] Downloading package omw-1.4 to C:\\Users\\Visakh H\n",
      "[nltk_data]     S\\AppData\\Roaming\\nltk_data...\n",
      "[nltk_data]   Package omw-1.4 is already up-to-date!\n"
     ]
    }
   ],
   "source": [
    "# Download NLTK resources\n",
    "try:\n",
    "    nltk.data.find(\"corpora/stopwords\")\n",
    "except LookupError:\n",
    "    nltk.download(\"stopwords\")\n",
    "\n",
    "try:\n",
    "    nltk.data.find(\"corpora/wordnet\")\n",
    "except LookupError:\n",
    "    nltk.download(\"wordnet\")\n",
    "\n",
    "try:\n",
    "    nltk.data.find(\"corpora/omw-1.4\")\n",
    "except LookupError:\n",
    "    nltk.download(\"omw-1.4\")"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 47,
   "id": "a9553346-409b-4266-b519-ba74dc43b3a8",
   "metadata": {},
   "outputs": [],
   "source": [
    "stop_words = set(stopwords.words(\"english\"))\n",
    "lemmatizer = WordNetLemmatizer()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 48,
   "id": "d1c0c1a1-4947-418c-a582-7a3c28071610",
   "metadata": {},
   "outputs": [],
   "source": [
    "# Clean job titles and descriptions for NLP.\n",
    "def clean_text(text):\n",
    "\n",
    "    if pd.isna(text):\n",
    "        return \"\"\n",
    "\n",
    "    original_text = str(text)   # Save original text\n",
    "\n",
    "    text = original_text\n",
    "\n",
    "    # Remove HTML\n",
    "    text = BeautifulSoup(text, \"html.parser\").get_text(separator=\" \")\n",
    "\n",
    "    # Lowercase\n",
    "    text = text.lower()\n",
    "\n",
    "    # Remove URLs\n",
    "    text = re.sub(r\"http\\S+|www\\S+\", \" \", text)\n",
    "\n",
    "    # Remove email addresses\n",
    "    text = re.sub(r\"\\S+@\\S+\", \" \", text)\n",
    "\n",
    "    # Remove punctuation & numbers\n",
    "    text = re.sub(r\"[^a-z\\s]\", \" \", text)\n",
    "\n",
    "    # Remove extra whitespace\n",
    "    text = re.sub(r\"\\s+\", \" \", text).strip()\n",
    "\n",
    "    words = text.split()\n",
    "\n",
    "    words = [\n",
    "        lemmatizer.lemmatize(word)\n",
    "        for word in words\n",
    "        if word not in stop_words\n",
    "        and len(word) > 1\n",
    "    ]\n",
    "\n",
    "    cleaned = \" \".join(words)\n",
    "\n",
    "    # If everything was removed, return the original title\n",
    "    if cleaned == \"\":\n",
    "        return original_text\n",
    "    return cleaned"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 49,
   "id": "78b97f98-2da6-42c1-80a1-d1fdee43281c",
   "metadata": {},
   "outputs": [],
   "source": [
    "def main():\n",
    "\n",
    "    logger.info(\"=\" * 70)\n",
    "    logger.info(\"STARTING NLP PREPROCESSING\")\n",
    "    logger.info(\"=\" * 70)\n",
    "\n",
    "    df = pd.read_csv(MASTER_DATASET)\n",
    "\n",
    "    logger.info(f\"Loaded {len(df):,} jobs.\")\n",
    "\n",
    "    logger.info(\"Cleaning job titles...\")\n",
    "    df[\"title_clean\"] = df[\"title\"].apply(clean_text)\n",
    "\n",
    "    logger.info(\"Cleaning job descriptions...\")\n",
    "    df[\"description_clean\"] = df[\"description\"].apply(clean_text)\n",
    "\n",
    "    output_file = MASTER_DATASET.with_name(\n",
    "    MASTER_DATASET.stem + \"_nlp.csv\"\n",
    ")\n",
    "\n",
    "    df.to_csv(output_file, index=False)\n",
    "\n",
    "    logger.info(f\"NLP dataset saved to:\\n{output_file}\")\n",
    "\n",
    "    logger.info(\"=\" * 70)\n",
    "    logger.info(\"NLP PREPROCESSING COMPLETED\")\n",
    "    logger.info(\"=\" * 70)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 50,
   "id": "6a4d0350-a063-4e3d-8874-f59c6d7b65f8",
   "metadata": {},
   "outputs": [
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "2026-07-29 22:21:20 | INFO | ======================================================================\n",
      "2026-07-29 22:21:20 | INFO | STARTING NLP PREPROCESSING\n",
      "2026-07-29 22:21:20 | INFO | ======================================================================\n",
      "2026-07-29 22:21:21 | INFO | Loaded 19,207 jobs.\n",
      "2026-07-29 22:21:21 | INFO | Cleaning job titles...\n",
      "2026-07-29 22:21:24 | INFO | Cleaning job descriptions...\n",
      "2026-07-29 22:21:32 | INFO | NLP dataset saved to:\n",
      "C:\\Users\\Visakh H S\\Labour_Market_Intelligence\\data\\processed\\master_jobs_nlp.csv\n",
      "2026-07-29 22:21:32 | INFO | ======================================================================\n",
      "2026-07-29 22:21:32 | INFO | NLP PREPROCESSING COMPLETED\n",
      "2026-07-29 22:21:32 | INFO | ======================================================================\n"
     ]
    }
   ],
   "source": [
    "if __name__ == \"__main__\":\n",
    "    main()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 51,
   "id": "6452d340-0966-41bb-bc7b-8dc77fb85c72",
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "C:\\Users\\Visakh H S\\Labour_Market_Intelligence\\data\\processed\\master_jobs_nlp.csv\n",
      "True\n"
     ]
    }
   ],
   "source": [
    "# test the output file\n",
    "from pathlib import Path\n",
    "\n",
    "output_file = MASTER_DATASET.with_name(\n",
    "    MASTER_DATASET.stem + \"_nlp.csv\"\n",
    ")\n",
    "\n",
    "print(output_file)\n",
    "print(output_file.exists())"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 57,
   "id": "338dd234-7910-415a-9d8c-2ddd0ce6acea",
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "(19207, 16)\n"
     ]
    }
   ],
   "source": [
    "import pandas as pd\n",
    "\n",
    "df = pd.read_csv(output_file)\n",
    "\n",
    "print(df.shape)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 59,
   "id": "e87fc0b4-cb11-45c8-8d03-5ee5084c5b76",
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/html": [
       "<div>\n",
       "<style scoped>\n",
       "    .dataframe tbody tr th:only-of-type {\n",
       "        vertical-align: middle;\n",
       "    }\n",
       "\n",
       "    .dataframe tbody tr th {\n",
       "        vertical-align: top;\n",
       "    }\n",
       "\n",
       "    .dataframe thead th {\n",
       "        text-align: right;\n",
       "    }\n",
       "</style>\n",
       "<table border=\"1\" class=\"dataframe\">\n",
       "  <thead>\n",
       "    <tr style=\"text-align: right;\">\n",
       "      <th></th>\n",
       "      <th>title</th>\n",
       "      <th>title_clean</th>\n",
       "      <th>description</th>\n",
       "      <th>description_clean</th>\n",
       "    </tr>\n",
       "  </thead>\n",
       "  <tbody>\n",
       "    <tr>\n",
       "      <th>0</th>\n",
       "      <td>Dispenser NVQ</td>\n",
       "      <td>dispenser nvq</td>\n",
       "      <td>Join Our Superdrug Pharmacy Team Whether You'r...</td>\n",
       "      <td>join superdrug pharmacy team whether qualified...</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>1</th>\n",
       "      <td>Service Colleague Express</td>\n",
       "      <td>service colleague express</td>\n",
       "      <td>Job Title Service Colleague (Express) Location...</td>\n",
       "      <td>job title service colleague express location e...</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>2</th>\n",
       "      <td>Service Colleague Express</td>\n",
       "      <td>service colleague express</td>\n",
       "      <td>Job Title Service Colleague (Express) Location...</td>\n",
       "      <td>job title service colleague express location e...</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>3</th>\n",
       "      <td>Customer Delivery Driver</td>\n",
       "      <td>customer delivery driver</td>\n",
       "      <td>Job Title Customer Delivery Driver Location St...</td>\n",
       "      <td>job title customer delivery driver location st...</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>4</th>\n",
       "      <td>IT Security Technical Delivery Manager VP</td>\n",
       "      <td>security technical delivery manager vp</td>\n",
       "      <td>My leading Banking client are looking for a ta...</td>\n",
       "      <td>leading banking client looking talented motiva...</td>\n",
       "    </tr>\n",
       "  </tbody>\n",
       "</table>\n",
       "</div>"
      ],
      "text/plain": [
       "                                       title  \\\n",
       "0                              Dispenser NVQ   \n",
       "1                  Service Colleague Express   \n",
       "2                  Service Colleague Express   \n",
       "3                   Customer Delivery Driver   \n",
       "4  IT Security Technical Delivery Manager VP   \n",
       "\n",
       "                              title_clean  \\\n",
       "0                           dispenser nvq   \n",
       "1               service colleague express   \n",
       "2               service colleague express   \n",
       "3                customer delivery driver   \n",
       "4  security technical delivery manager vp   \n",
       "\n",
       "                                         description  \\\n",
       "0  Join Our Superdrug Pharmacy Team Whether You'r...   \n",
       "1  Job Title Service Colleague (Express) Location...   \n",
       "2  Job Title Service Colleague (Express) Location...   \n",
       "3  Job Title Customer Delivery Driver Location St...   \n",
       "4  My leading Banking client are looking for a ta...   \n",
       "\n",
       "                                   description_clean  \n",
       "0  join superdrug pharmacy team whether qualified...  \n",
       "1  job title service colleague express location e...  \n",
       "2  job title service colleague express location e...  \n",
       "3  job title customer delivery driver location st...  \n",
       "4  leading banking client looking talented motiva...  "
      ]
     },
     "execution_count": 59,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "# to check the first 5 data from output file\n",
    "df = pd.read_csv(output_file)\n",
    "\n",
    "df[[\n",
    "    \"title\",\n",
    "    \"title_clean\",\n",
    "    \"description\",\n",
    "    \"description_clean\"\n",
    "]].head(5)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 58,
   "id": "8333da08-6597-40d3-b178-b717c88184ca",
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "0\n",
      "0\n"
     ]
    }
   ],
   "source": [
    "# to check whether there is any null values in output file\n",
    "print(df[\"title_clean\"].isna().sum())\n",
    "print(df[\"description_clean\"].isna().sum())"
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3 (ipykernel)",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.13.9"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 5
}
