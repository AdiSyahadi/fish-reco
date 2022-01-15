# Core Pkg
import streamlit as st 
import streamlit.components.v1 as stc 
from PIL import Image


# Load EDA
import pandas as pd 
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity,linear_kernel


# Load Our Dataset
def load_data(data):
	df = pd.read_csv(data)
	return df 


# Fxn
# Vectorize + Cosine Similarity Matrix

def vectorize_text_to_cosine_mat(data):
	count_vect = CountVectorizer()
	cv_mat = count_vect.fit_transform(data)
	# Get the cosine
	cosine_sim_mat = cosine_similarity(cv_mat)
	return cosine_sim_mat



# Recommendation Sys
@st.cache
def get_recommendation(title,cosine_sim_mat,df,num_of_rec=96):
	# indices of the course
	course_indices = pd.Series(df.index,index=df['nama_ikan']).drop_duplicates()
	# Index of course
	idx = course_indices[title]

	# Look into the cosine matr for that index
	sim_scores =list(enumerate(cosine_sim_mat[idx]))
	sim_scores = sorted(sim_scores,key=lambda x: x[1],reverse=True)
	selected_course_indices = [i[0] for i in sim_scores[1:]]
	selected_course_scores = [i[0] for i in sim_scores[1:]]

	# Get the dataframe & title
	result_df = df.iloc[selected_course_indices]
	result_df['similarity_score'] = selected_course_scores
	final_recommended_courses = result_df[['nama_ikan','url','price','penjual','num_rate']]
	return final_recommended_courses.head(num_of_rec)


RESULT_TEMP = """
<div style="width:90%;height:100%;margin:1px;padding:5px;position:relative;border-radius:5px;
 background-color: #d1d8e0;
  border-left: 5px solid #a5b1c2;">
<h2>{}</h2>
<p style="color:blue;"><span style="color:black;"><img src="https://img.icons8.com/office/16/000000/shop.png"/> : </span><a href="{}",target="_blank">Link Store</a></p>
<p style="color:blue;"><span style="color:black;">Harga : </span>{}</p>
<p style="color:blue;"><span style="color:black;">Penjual : </span>{}</p>
<p style="color:blue;"><span style="color:black;">Terjual : </span>{}</p>

</div>
"""

# Search For Course 
@st.cache
def search_term_if_not_found(term,df):
	result_df = df[df['nama_ikan'].str.contains(term)]
	return result_df


def main():

	st.title("Fish Recommendation App")

	menu = ["Home","Recommend","About"]
	choice = st.sidebar.selectbox("Menu",menu)

	df = load_data("data/udemy_course_data.csv")

	if choice == "Home":
		st.subheader("Home")
		st.title('This is a title')
		col1, col2, col3 = st.columns(3)

		with col1:
		    st.header("Ikan Patin")
		    st.image("https://cdn.idntimes.com/content-images/community/2019/03/ikan-tuna-337d58f37de71665001b5431308e58ae_600x400.jpg")

		with col2:
		    st.header("Ikan Bandeng")
		    st.image("https://1.bp.blogspot.com/-leyZ6FE41_4/XBIcPe0NN2I/AAAAAAAAGPM/QZQHSskDDKkrCxRprHYmG5IxO-WOs-lIwCLcBGAs/s1600/1.jpg")

		with col3:
		    st.header("Ikan Teri")
		    st.image("https://cdnt.orami.co.id/unsafe/cdn-cas.orami.co.id/parenting/images/teri.width-800.jpegquality-80.jpg")
		
		st.dataframe(df.head())


	elif choice == "Recommend":
		st.subheader("Recommend Fish")
		cosine_sim_mat = vectorize_text_to_cosine_mat(df['nama_ikan'])
		search_term = st.text_input("Search")
		num_of_rec = st.sidebar.number_input("Number",4,30,7)
		if st.button("Recommend"):
			if search_term is not None:
				try:
					results = get_recommendation(search_term,cosine_sim_mat,df,num_of_rec)
					with st.beta_expander("Results as JSON"):
						results_json = results.to_dict('index')
						st.write(results_json)

					for row in results.iterrows():
						rec_title = row[1][0]
						rec_url = row[1][1]
						rec_price = row[1][2]
						rec_penjual = row[1][3]
						rec_num_rate = row[1][4]

						# st.write("Title",rec_title,)
						stc.html(RESULT_TEMP.format(rec_title,rec_url,rec_price,rec_penjual,rec_num_rate),height=350)
				except:
					results= "Not Found"
					st.warning(results)
					st.info("Suggested Options include")
					result_df = search_term_if_not_found(search_term,df)
					st.dataframe(result_df)



				# How To Maximize Your Profits Options Trading




	else:
		st.subheader("About")
		st.text("Built with Streamlit & Pandas")


if __name__ == '__main__':
	main()


